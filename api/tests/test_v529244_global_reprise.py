from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
def test_j244_clean_single_viewport_authority():
 assert 'allroads-v52947-pwa-stability' not in HTML
 assert 'JEPALYSShell244' in HTML
 assert 'ancien verrou de coque neutralisé' in HTML
def test_j244_home_landscape_reflow():
 assert 'grid-template-columns:minmax(0,52%) minmax(0,48%)' in HTML
 assert '.ar-home-selected-card{grid-column:1!important;grid-row:3!important' in HTML
 assert '#vsflat-home-actions{grid-column:2!important;grid-row:2/4!important' in HTML
def test_j244_keyboard_retracts_after_place_selection():
 assert "k.classList.add('place-selected');compareDestinationInKeyboard()" in HTML
 assert '#vs207-keyboard.place-selected #vs207-kb-keys' in HTML
def test_j244_driving_landscape_no_overlap_contract():
 assert 'height:112px!important;min-height:112px!important' in HTML
 assert 'bottom:92px!important;left:12px!important' in HTML
 assert '.ar51-center-map{top:282px!important' in HTML
def test_j244_route_compromise():
 assert "className:'ar-driving-route-core'" in HTML
 assert "className:'ar-driving-route-core',color:'#0A7BFF',weight:Math.min(48,weight+3.2)" in HTML
def test_j244_mirrors():
 assert (ROOT/'api/frontend/index.html').read_bytes()==(ROOT/'frontend/index.html').read_bytes()
 assert (ROOT/'api/frontend/sw.js').read_bytes()==(ROOT/'frontend/sw.js').read_bytes()
