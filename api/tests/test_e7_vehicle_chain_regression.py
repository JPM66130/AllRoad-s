from pathlib import Path
HTML=(Path(__file__).parents[1]/"frontend"/"index.html").read_text(encoding="utf-8")

def test_vehicle_to_prepare_chain_has_no_intermediate_prepare_overlay():
    assert '<div id="ar-e7-prepare-map"' not in HTML
    proceed=HTML.split('function proceed(){',1)[1].split("document.getElementById('ar52-home')",1)[0]
    assert "window.AllRoadsMobileNav.open(profile)" in proceed
    nav_start=HTML.index('function open(p){', HTML.index('const demoCoords='))
    nav=HTML[nav_start:HTML.index('function close(){',nav_start)]
    assert "document.body.classList.add('ar-mobile-nav-open')" in nav
    assert "panel('prepare')" in nav
