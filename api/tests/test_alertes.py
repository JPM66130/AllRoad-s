from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import api.main as main
from db import Base, get_db
from models.alertes import Alerte


def _client_with_alert():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = Session()
    alerte = Alerte(titre="Travaux", message="Route barrée", profils_csv="bus", niveau="warning", actif=True)
    db.add(alerte)
    db.commit()
    db.refresh(alerte)
    alert_id = alerte.id
    db.close()

    def override_get_db():
        session = Session()
        try:
            yield session
        finally:
            session.close()

    main.app.dependency_overrides[get_db] = override_get_db
    return TestClient(main.app, client=("127.0.0.1", 50000)), engine, alert_id


def test_get_alertes():
    client, engine, _ = _client_with_alert()
    try:
        response = client.get("/alertes")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 1
    finally:
        main.app.dependency_overrides.clear()
        engine.dispose()


def test_get_alerte_by_id():
    client, engine, alert_id = _client_with_alert()
    try:
        response = client.get(f"/alertes/{alert_id}")
        assert response.status_code == 200
        body = response.json()
        assert body["titre"] == "Travaux"
        assert body["niveau"] == "warning"
    finally:
        main.app.dependency_overrides.clear()
        engine.dispose()
