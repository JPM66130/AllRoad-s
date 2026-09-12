"""Contrôle groupé local du bloc Fonctions chauffeur.

Un seul scénario couvre : noms nettoyés, arrêts bus, historique limité à 20
et compteur général cumulatif au-delà de l'historique conservé.
Aucun service de routage externe n'est appelé.
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


def _route_demo():
    return {
        "distance_km": 10.0,
        "duree_min": 15.0,
        "source": "local-test",
        "profil_ors": "car",
        "steps": [],
        "geometry": {"type": "LineString", "coordinates": [[2.89, 42.69], [2.88, 42.68]]},
    }


def _client_memory():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = factory()
        try:
            yield db
        finally:
            db.close()

    main.app.dependency_overrides[get_db] = override_get_db
    return TestClient(main.app, client=("127.0.0.1", 50000)), engine


@pytest.mark.chauffeur
def test_bloc_fonctions_chauffeur():
    client, engine = _client_memory()
    try:
        with patch.object(itineraires_router, "calcul_itineraire", return_value=_route_demo()):
            ids = []
            for index in range(22):
                response = client.get(
                    "/itineraire/calcul",
                    params={"lat1": 42.69, "lon1": 2.89, "lat2": 42.68, "lon2": 2.88, "profil": "bus"},
                )
                assert response.status_code == 200
                ids.append(response.json()["itineraire_id"])

        # L'historique reste léger : 20 dernières tournées seulement.
        historique = client.get("/itineraire/")
        assert historique.status_code == 200
        assert len(historique.json()) == 20
        assert historique.json()[0]["id"] == ids[-1]
        assert ids[0] not in [item["id"] for item in historique.json()]

        # Le compteur, lui, continue à cumuler tous les trajets.
        compteur = client.get("/itineraire/compteur")
        assert compteur.status_code == 200
        assert compteur.json() == {"total_km": 220.0, "trajets": 22}

        # Noms nettoyés et blancs refusés.
        rename = client.put(f"/itineraire/{ids[-1]}/tournee", json={"nom_tournee": "  Ligne scolaire  "})
        assert rename.status_code == 200
        assert rename.json()["nom_tournee"] == "Ligne scolaire"
        assert client.put(f"/itineraire/{ids[-1]}/tournee", json={"nom_tournee": "   "}).status_code == 422

        arret = client.post(
            f"/itineraire/{ids[-1]}/arrets",
            json={"nom": "  Collège  ", "latitude": 42.685, "longitude": 2.885, "direction_deg": 180, "precision_m": 5},
        )
        assert arret.status_code == 200
        assert arret.json()["nom"] == "Collège"
        assert client.post(
            f"/itineraire/{ids[-1]}/arrets",
            json={"nom": "   ", "latitude": 42.685, "longitude": 2.885, "direction_deg": 180, "precision_m": 5},
        ).status_code == 422
    finally:
        main.app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
