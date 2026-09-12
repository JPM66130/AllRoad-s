from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend'/'index.html').read_text(encoding='utf-8')

def test_v66_release_identity():
    assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'
    assert (ROOT/'AA_LANCER_JEPALYS.bat').exists()
    assert 'APP_VERSION = "V52.9.102"' in (ROOT/'api'/'main.py').read_text(encoding='utf-8')

def test_v66_landscape_order_is_final_and_explicit():
    marker='allroads-v52966-landscape-driving-order-test'
    assert marker in HTML
    block=HTML[HTML.index(marker):]
    assert '#ar-mobile-nav[data-state="driving"] .ar525-mapviews' in block
    assert 'top:46px!important' in block
    assert '#ar-mobile-nav[data-state="driving"] .ar51-maneuver' in block
    assert 'top:94px!important' in block
    assert HTML.index(marker) > HTML.index('allroads-v52960-driving-order')

def test_v66_vehicle_landscape_is_compact_no_scroll():
    block=HTML[HTML.index('allroads-v52966-landscape-driving-order-test'):]
    assert 'grid-template-rows:38px 30px 52px 36px 84px 42px!important' in block
    assert 'align-content:start!important;overflow:hidden!important' in block
    assert 'height:84px!important;min-height:84px!important;max-height:84px!important' in block

def test_frontend_mirrors_match():
    assert (ROOT/'frontend'/'index.html').read_bytes()==(ROOT/'api'/'frontend'/'index.html').read_bytes()
