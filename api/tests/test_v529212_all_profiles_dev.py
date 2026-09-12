from pathlib import Path
from routers import access

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = (ROOT / 'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8')
HTML = (ROOT / 'api/frontend/index.html').read_text(encoding='utf-8')


def test_j212_main_launcher_unlocks_all_profiles_only_for_local_dev(monkeypatch):
    assert 'set "ALLROADS_ACCESS_STATE=PRO"' in LAUNCHER
    assert 'set "ENVIRONMENT=development"' in LAUNCHER
    assert 'Mode développeur : <strong>8 profils accessibles</strong>' in HTML
    monkeypatch.setenv('ALLROADS_ACCESS_STATE', 'PRO')
    snap = access.access_snapshot()
    assert set(snap['unlocked_profiles']) == set(access.ALL_PROFILES)
    for profile in access.ALL_PROFILES:
        assert access.require_profile_access(profile)['service_enabled'] is True


def test_j212_commercial_default_is_not_weakened(monkeypatch):
    monkeypatch.delenv('ALLROADS_ACCESS_STATE', raising=False)
    snap = access.access_snapshot()
    assert snap['state'] == 'TEST'
    assert set(snap['unlocked_profiles']) == {'voiture', 'bus'}
