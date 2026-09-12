from pathlib import Path

from fastapi.testclient import TestClient

import main
from routers import access


ROOT = Path(__file__).resolve().parents[2]
HTML = (ROOT / 'api' / 'frontend' / 'index.html').read_text(encoding='utf-8')


def test_j237_owner_and_tester_rights_are_separate(monkeypatch):
    monkeypatch.setenv('ALLROADS_ACCESS_STATE', 'TEST')
    tester = access.access_snapshot('tester')
    owner = access.access_snapshot('owner')
    assert tester['role'] == 'tester'
    assert set(tester['unlocked_profiles']) == {'voiture', 'bus'}
    assert owner['role'] == 'owner'
    assert set(owner['unlocked_profiles']) == set(access.ALL_PROFILES)


def test_j237_frontend_no_longer_unlocks_all_profiles_on_internet():
    assert 'const ALLROADS_DEV_ALL_PROFILES = isLocalApi;' in HTML
    assert "Accès J237" in HTML


def test_j237_entry_pages_set_role_cookie(monkeypatch):
    monkeypatch.setattr(main, 'TESTER_ACCESS_TOKEN', 'tester-secret')
    monkeypatch.setattr(main, 'OWNER_ACCESS_TOKEN', 'owner-secret')
    client = TestClient(main.app)

    tester = client.get('/essais-route/tester-secret')
    assert tester.status_code == 200
    assert 'Essais route' in tester.text
    assert main.ACCESS_COOKIE in tester.cookies

    owner = client.get('/acces-interne/owner-secret')
    assert owner.status_code == 200
    assert 'Accès personnel complet' in owner.text
    assert main.ACCESS_COOKIE in owner.cookies

    bad = client.get('/essais-route/mauvais')
    assert bad.status_code == 404
