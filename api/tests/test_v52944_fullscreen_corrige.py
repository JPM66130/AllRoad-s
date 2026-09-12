from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HTML = (ROOT / "frontend" / "index.html").read_text(encoding="utf-8")

def test_version_and_launcher_44():
    assert (ROOT / "VERSION_DEMO.txt").read_text(encoding="utf-8").strip() == "V52.9.102"
    launchers = list(ROOT.glob('*LANCER_ALLROADS_V52_9_*.bat'))
    assert len(launchers) == 1
    assert launchers[0].name == "AA_LANCER_JEPALYS.bat"

def test_fullscreen_control_is_user_triggered_and_not_orientation_forced():
    assert 'id="ar-fullscreen-trigger"' in HTML
    assert 'id="allroads-v52944-fullscreen-js"' in HTML
    assert "requestFullscreen({ navigationUI: 'hide' })" in HTML
    assert "webkitRequestFullscreen" in HTML
    block = HTML.split('id="allroads-v52944-fullscreen-js"', 1)[1]
    assert 'orientation.lock' not in block

def test_fullscreen_cleans_demo_chrome_without_changing_views():
    assert 'html.ar-fullscreen-active #ar-fullscreen-trigger' in HTML
    assert 'html.ar-fullscreen-active #ar-dev-profile-access' in HTML
    assert "window.dispatchEvent(new Event(\'resize\'))" in HTML
    assert 'allroads-v52942-home-landscape-harmonise' in HTML
    assert '#ar-mobile-nav[data-state="ready"] .ar51-sheet' in HTML
    assert '#ar-mobile-nav[data-state="driving"]' in HTML

def test_frontend_copies_identical_v52944():
    assert (ROOT / "frontend" / "index.html").read_bytes() == (ROOT / "api/frontend" / "index.html").read_bytes()


def test_v52944_home_visibility_does_not_hide_fullscreen_controls():
    html = HTML
    selector = 'body.ar-mobile-home-open > *:not(#allroads-mobile-home):not(#ar-fullscreen-trigger):not(#ar-fullscreen-status):not(#ar-pwa-install){visibility:hidden!important;}'
    assert selector in html
    assert 'body.ar-mobile-home-open > *:not(#allroads-mobile-home){visibility:hidden!important;}' not in html
