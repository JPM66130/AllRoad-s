"""Tests groupés du bloc Navigation / Itinéraire AllRoads.

Objectif : valider en une seule suite le parcours fonctionnel principal utilisé
pendant les essais chauffeur, sans dépendre d'un service de routage externe.
"""

from unittest.mock import patch

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import api.main as main
import routers.itineraires as itineraires_router
from db import Base, get_db


def _route_bus_demo():
    return {
        "distance_km": 12.5,
        "duree_min": 18.0,
        "source": "graphhopper",
        "profil_ors": "car",
        "steps": [
            {"instruction": "Continuer tout droit", "distance_km": 5.0, "duree_min": 7.0},
            {"instruction": "Tourner à droite", "distance_km": 7.5, "duree_min": 11.0},
        ],
        "geometry": {
            "type": "LineString",
            "coordinates": [[2.8954, 42.6986], [2.8862, 42.6960], [2.8650, 42.6880]],
        },
    }


def _client_with_memory_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    main.app.dependency_overrides[get_db] = override_get_db
    return TestClient(main.app, client=("127.0.0.1", 50000)), engine


@pytest.mark.navigation
def test_parcours_chauffeur_bus_de_bout_en_bout():
    client, engine = _client_with_memory_db()
    try:
        # 1. Le profil bus expose bien ses contraintes connues.
        profils = client.get("/itineraire/profils")
        assert profils.status_code == 200
        assert profils.json()["bus"]["hauteur_m"] == 4.0
        assert profils.json()["bus"]["largeur_m"] == 2.6
        assert profils.json()["bus"]["longueur_m"] == 18.0
        assert profils.json()["bus"]["poids_max_t"] == 19.0

        # 2. Calcul d'un trajet bus (moteur simulé pour rendre le test stable et gratuit).
        with patch.object(itineraires_router, "calcul_itineraire", return_value=_route_bus_demo()):
            calcul = client.get(
                "/itineraire/calcul",
                params={
                    "lat1": 42.6986,
                    "lon1": 2.8954,
                    "lat2": 42.6880,
                    "lon2": 2.8650,
                    "profil": "bus",
                    "vitesse": 110,
                },
            )

        assert calcul.status_code == 200
        trajet = calcul.json()
        trajet_id = trajet["itineraire_id"]
        assert trajet["profil"] == "bus"
        assert trajet["vitesse_kmh"] == 90  # plafond du profil bus
        assert trajet["geometry"]["type"] == "LineString"
        assert len(trajet["etapes"]) == 2
        assert trajet["avertissements_routage"]  # garde-fou : ce n'est pas encore un GPS bus certifié

        # 3. Nommer la tournée.
        tournee = client.put(
            f"/itineraire/{trajet_id}/tournee",
            json={"nom_tournee": "Test Perpignan - ligne scolaire"},
        )
        assert tournee.status_code == 200
        assert tournee.json()["nom_tournee"] == "Test Perpignan - ligne scolaire"

        # 4. Enregistrer un arrêt chauffeur avec sens de circulation.
        arret = client.post(
            f"/itineraire/{trajet_id}/arrets",
            json={
                "nom": "Arrêt test",
                "latitude": 42.6960,
                "longitude": 2.8862,
                "direction_deg": 225.0,
                "precision_m": 4.0,
            },
        )
        assert arret.status_code == 200
        assert arret.json()["nom"] == "Arrêt test"

        # 5. L'historique restitue tournée + profil + géométrie + arrêt.
        historique = client.get("/itineraire/")
        assert historique.status_code == 200
        sauvegarde = historique.json()[0]
        assert sauvegarde["id"] == trajet_id
        assert sauvegarde["profil"] == "bus"
        assert sauvegarde["nom_tournee"] == "Test Perpignan - ligne scolaire"
        assert sauvegarde["geometry"]["type"] == "LineString"
        assert sauvegarde["arrets"][0]["nom"] == "Arrêt test"

        # 6. Le compteur tient compte du trajet créé.
        compteur = client.get("/itineraire/compteur")
        assert compteur.status_code == 200
        assert compteur.json()["trajets"] == 1
        assert compteur.json()["total_km"] == 12.5
    finally:
        main.app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
