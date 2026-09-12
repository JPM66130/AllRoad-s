from pathlib import Path
HTML = Path(__file__).parents[1] / "frontend" / "index.html"

def test_failed_prepare_surface_experiment_is_rolled_back():
    text = HTML.read_text(encoding="utf-8")
    assert '<div id="ar-e7-prepare-map"' not in text
    assert 'let arE7PrepareMap=' not in text
    assert 'id="map"' in text

def test_ready_and_driving_keep_main_route_map():
    text = HTML.read_text(encoding="utf-8")
    assert 'body.ar-mobile-nav-open #map{display:block!important;visibility:visible!important;opacity:1!important}' in text
    assert 'body[data-ar-visual-mode="demo"] #map{display:none!important}' in text
