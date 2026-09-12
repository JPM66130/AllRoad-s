from pathlib import Path
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
HTML = (ROOT / 'api' / 'frontend' / 'index.html').read_text(encoding='utf-8')


def test_v52951_version_and_launcher():
    assert (ROOT / 'VERSION_DEMO.txt').read_text(encoding='utf-8').strip() == 'V52.9.102'
    launchers = list(ROOT.glob('*LANCER_ALLROADS*.bat'))
    assert len(launchers) == 1
    assert launchers[0].name == 'AA_LANCER_JEPALYS.bat'


def test_keyboard_controller_keeps_destination_visible():
    assert 'allroads-v52951-keyboard-safe-input' in HTML
    assert 'allroads-v52951-keyboard-safe-input-js' in HTML
    assert '--ar-keyboard-inset' in HTML
    assert 'ar-keyboard-open' in HTML
    assert "function routeEditable(el)" in HTML
    assert "textarea,[contenteditable=\"true\"]" in HTML
    assert "setTimeout(dismissKeyboard,0)" in HTML
    assert "button,a,[role=\"button\"],select,label[for]" in HTML
    assert "window.AllRoadsDismissKeyboard=dismissKeyboard" in HTML
    assert 'ar-global-input-bar' in HTML
    assert "root.classList.add('ar-global-input-active')" in HTML
    assert 'scrollIntoView' not in HTML


def test_only_keyboard_controller_uses_visualviewport_resize():
    # Un seul abonnement resize visualViewport : celui du clavier. La coque
    # principale ne doit plus être pilotée par deux contrôleurs concurrents.
    assert HTML.count("visualViewport.addEventListener('resize'") == 1
    assert "visualViewport n'a volontairement AUCUN droit de redimensionner la coque" in HTML


def test_stale_usage_heartbeat_is_idempotent_200():
    from api.main import app
    client = TestClient(app)
    response = client.post('/usage/session/heartbeat', json={'session_id': 'session-stale-v52951'})
    assert response.status_code == 200
    data = response.json()
    assert data['ok'] is False
    assert data['stale'] is True

def test_service_worker_cache_rotated_for_v52951():
    sw=(ROOT/'api'/'frontend'/'sw.js').read_text(encoding='utf-8')
    assert "allroads-v52-9-95" in sw
    assert (ROOT/'api'/'frontend'/'sw.js').read_bytes()==(ROOT/'frontend'/'sw.js').read_bytes()
