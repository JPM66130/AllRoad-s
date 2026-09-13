from fastapi.testclient import TestClient

import main
import routers.poi as poi


def test_j240_named_poi_uses_geocoder(monkeypatch):
    monkeypatch.setattr(poi, "geocoder", lambda q, focus_lat=None, focus_lon=None: [
        {"nom": "Carrefour Perpignan", "latitude": 42.70, "longitude": 2.89, "pays": "France"}
    ])
    client = TestClient(main.app)
    r = client.get("/poi/search", params={"q": "Carrefour Perpignan", "lat": 42.67, "lon": 2.62})
    assert r.status_code == 200
    data = r.json()
    assert data[0]["nom"] == "Carrefour Perpignan"
    assert data[0]["source"] == "ors-pelias"


def test_j240_category_requires_position():
    client = TestClient(main.app)
    r = client.get("/poi/search", params={"category": "parking"})
    assert r.status_code == 400


def test_j240_overpass_query_covers_core_categories():
    assert 'amenity"="parking' in poi._overpass_query(42.6, 2.6, 10000, "parking")
    assert 'highway"="rest_area' in poi._overpass_query(42.6, 2.6, 10000, "rest_area")
    assert 'amenity"="fuel' in poi._overpass_query(42.6, 2.6, 10000, "fuel")

def test_j240_core_poi_categories_are_supported():
    for category in ("rest_area", "motorhome", "parking", "fuel", "lpg", "water_dump", "camping", "mall", "shop"):
        assert category in poi.CATEGORY_FILTERS
