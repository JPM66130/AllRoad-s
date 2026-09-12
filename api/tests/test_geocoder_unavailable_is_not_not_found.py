import json
from unittest.mock import patch
import pytest
from fastapi import HTTPException
from utils.geo import GeocodingUnavailable, geocoder
from routers.itineraires import rechercher_adresse


def test_geocoder_retries_transient_provider_failure(monkeypatch):
    monkeypatch.setattr('utils.geo._ors_api_key', lambda: 'key')
    payload = {"features": [{"properties": {"label": "Thuir, France", "country": "France"}, "geometry": {"coordinates": [2.758715, 42.629340]}}]}
    class R:
        def __enter__(self): return self
        def __exit__(self,*args): return False
        def read(self): return json.dumps(payload).encode()
    with patch('utils.geo.urllib.request.urlopen', side_effect=[OSError('réseau temporaire'), R()]) as mocked:
        places = geocoder('Thuir', focus_lat=42.67, focus_lon=2.62)
    assert mocked.call_count == 2
    assert places[0]['nom'] == 'Thuir, France'


def test_provider_failure_is_503_not_empty_address(monkeypatch):
    monkeypatch.setattr('utils.geo._ors_api_key', lambda: 'key')
    with patch('utils.geo.urllib.request.urlopen', side_effect=OSError('hors ligne')):
        with pytest.raises(GeocodingUnavailable):
            geocoder('Thuir', focus_lat=42.67, focus_lon=2.62)
    monkeypatch.setattr('routers.itineraires.geocoder', lambda *a, **k: (_ for _ in ()).throw(GeocodingUnavailable('Service de recherche d’adresse temporairement indisponible')))
    with pytest.raises(HTTPException) as caught:
        rechercher_adresse('Thuir', 42.67, 2.62)
    assert caught.value.status_code == 503
