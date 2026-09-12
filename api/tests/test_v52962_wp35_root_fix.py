from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend/index.html').read_text(encoding='utf-8')
API=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
def test_zoom_disabled_at_leaflet_source_and_globally():
    for text in (HTML,API):
        assert "L.map('map', {zoomControl:false" in text
        assert '.leaflet-control-zoom{display:none!important}' in text
def test_wp35_title_forced_single_line():
    assert 'font-size:20px!important;letter-spacing:-.55px!important;white-space:nowrap!important' in HTML
def test_immersive_reinforcement_is_not_automatic():
    assert 'requestFullscreen' in HTML
    assert "document.addEventListener('pointerup',reinforceImmersive" not in HTML
    assert "document.addEventListener('touchend',reinforceImmersive" not in HTML
    assert 'aucun plein écran automatique' in HTML
def test_frontend_mirrors_identical():
    assert HTML==API
