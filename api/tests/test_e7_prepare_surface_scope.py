from pathlib import Path
HTML = (Path(__file__).parents[1] / "frontend" / "index.html").read_text(encoding="utf-8")

def test_vehicle_continue_calls_mobile_navigation():
    block=HTML.split('function proceed(){',1)[1].split("document.getElementById('ar52-home')",1)[0]
    assert "document.body.classList.remove('ar52-vehicle-open')" in block
    assert "window.AllRoadsMobileNav.open(profile)" in block

def test_mobile_navigation_open_reaches_prepare():
    start=HTML.index('function open(p){', HTML.index('const demoCoords='))
    block=HTML[start:HTML.index('function close(){',start)]
    assert "document.body.classList.add('ar-mobile-nav-open')" in block
    assert "panel('prepare')" in block

def test_no_prepare_overlay_can_block_vehicle_screen():
    assert '#ar-e7-prepare-map' not in HTML
