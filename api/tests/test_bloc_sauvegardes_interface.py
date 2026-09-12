import os, sys
from pathlib import Path

os.environ["RATE_LIMIT_PER_MINUTE"] = "10000"
API = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(API))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import routers.itineraires as r

def fake(*args, **kwargs):
    return {"distance_km": 10.0, "duree_min": 10.0, "geometry": [[2.9,42.7],[2.91,42.71]], "source":"local-test", "profil_ors":"car", "steps":[]}

r.calcul_itineraire = fake
from fastapi.testclient import TestClient
from main import app
from db import Base, get_db


def test_sauvegardes_et_interface():
    # Test isolé : il ne dépend jamais des 20 sauvegardes éventuellement présentes
    # dans la base de développement copiée avec une version précédente.
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    def override_get_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    c = TestClient(app)
    try:
        x = c.get("/itineraire/calcul", params={"lat1":42.7,"lon1":2.9,"lat2":42.71,"lon2":2.91,"profil":"bus"})
        assert x.status_code == 200
        tid = x.json()["itineraire_id"]
        hist = c.get("/itineraire/").json()
        item = next(i for i in hist if i["id"] == tid)
        assert item["sauvegarde_volontaire"] is False
        s = c.put(f"/itineraire/{tid}/tournee", json={"nom_tournee":"Ligne test"})
        assert s.status_code == 200 and s.json()["sauvegarde_volontaire"] is True
        item = next(i for i in c.get("/itineraire/").json() if i["id"] == tid)
        assert item["sauvegarde_volontaire"] is True
        html = (API/"frontend/index.html").read_text(encoding="utf-8")
        assert "Trajet automatique" in html and "conservée" in html
    finally:
        app.dependency_overrides.pop(get_db, None)
