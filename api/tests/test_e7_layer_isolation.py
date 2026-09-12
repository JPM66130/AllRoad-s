from pathlib import Path
HTML = (Path(__file__).parents[1] / "frontend" / "index.html").read_text(encoding="utf-8")

def test_demo_canvas_is_not_inside_leaflet_map():
    map_id = HTML.index('id="map"')
    map_start = HTML.rfind('<section', 0, map_id)
    map_end = HTML.index('</section>', map_id)
    assert 'ar5296-drive-canvas' not in HTML[map_start:map_end]
    assert 'id="ar-e7-demo-layer"' in HTML

def test_demo_layer_is_fullscreen_and_separate():
    assert '#ar-e7-demo-layer{display:none;position:fixed;inset:0;z-index:710' in HTML
    assert '#ar-e7-demo-layer #ar5296-drive-canvas{display:block;width:100%;height:100%;position:absolute;inset:0' in HTML
    assert 'body[data-ar-visual-mode="demo"] #map{display:none!important}' in HTML
    assert 'body[data-ar-visual-mode="demo"] #ar-e7-demo-layer{display:block!important' in HTML

def test_e7_no_longer_hides_leaflet_panes():
    start = HTML.index('<style id="allroads-e7-visual-brick">')
    end = HTML.index('</style>', start)
    block = HTML[start:end]
    assert '.leaflet-map-pane' not in block
    assert '.leaflet-control-container' not in block
