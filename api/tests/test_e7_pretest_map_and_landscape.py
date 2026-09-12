from pathlib import Path
HTML = (Path(__file__).parents[1] / "frontend" / "index.html").read_text(encoding="utf-8")

def test_prepare_and_ready_use_leaflet_not_demo_canvas():
    assert 'body[data-ar-visual-mode="prepare"] #ar-e7-demo-layer' in HTML
    assert 'body[data-ar-visual-mode="ready"] #ar-e7-demo-layer' in HTML
    assert 'body.ar-mobile-nav-open #map{display:block!important;visibility:visible!important;opacity:1!important}' in HTML
