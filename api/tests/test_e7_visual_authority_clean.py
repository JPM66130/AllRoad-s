from pathlib import Path
HTML = (Path(__file__).parents[1] / "frontend" / "index.html").read_text(encoding="utf-8")

def test_one_visual_authority_block():
    assert HTML.count('id="allroads-e7-visual-brick"') == 1
    assert HTML.count('id="allroads-e7-visual-brick-js"') == 1

def test_prepare_ready_real_are_leaflet_and_demo_is_canvas():
    assert 'body.ar-mobile-nav-open #map{display:block!important;visibility:visible!important;opacity:1!important}' in HTML
    assert 'body[data-ar-visual-mode="demo"] #map{display:none!important}' in HTML
    assert 'body[data-ar-visual-mode="demo"] #ar-e7-demo-layer{display:block!important' in HTML

def test_prepare_is_europe_on_main_map():
    block=HTML.split('function arE7RefreshState(state,attempt=0){',1)[1].split('function panel(state){',1)[0]
    assert "if(state==='prepare')" in block
    assert 'map.setView(arE7EuropeView.center,arE7EuropeView.zoom,{animate:false})' in block
