"""Test groupé local du bloc Données route AllRoads.

Aucun service externe n'est appelé. On vérifie uniquement la cohérence des
routes locales et le jeu de stations livré avec le projet.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import api.main as main
from db import Base, get_db
from models.restrictions import Restriction


@pytest.mark.data_route
def test_bloc_donnees_route_local():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Une donnée locale suffit pour vérifier aussi l'accès par identifiant.
    db = session_factory()
    db.add(Restriction(type="hauteur", description="Exemple local"))
    db.commit()
    db.close()

    def override_get_db():
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    main.app.dependency_overrides[get_db] = override_get_db
    client = TestClient(main.app, client=("127.0.0.1", 50001))

    try:
        # Les six listes du bloc répondent sans dépendance externe.
        for route in ("restrictions", "alertes", "peages", "stations", "parkings", "spots"):
            response = client.get(f"/{route}/")
            assert response.status_code == 200
            assert isinstance(response.json(), list)

        # Les stations locales fournies avec AllRoads sont maintenant réellement exposées.
        stations = client.get("/stations/").json()
        assert len(stations) >= 3
        assert stations[0]["nom"] == "Aire de Perpignan Nord"
        assert "lat" in stations[0] and "lon" in stations[0]

        station = client.get("/stations/1")
        assert station.status_code == 200
        assert station.json()["ville"] == "Perpignan"

        # Accès individuel cohérent pour une table alimentée.
        restriction = client.get("/restrictions/1")
        assert restriction.status_code == 200
        assert restriction.json()["type"] == "hauteur"

        # Une ressource inconnue renvoie clairement 404.
        assert client.get("/parkings/9999").status_code == 404
    finally:
        main.app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
