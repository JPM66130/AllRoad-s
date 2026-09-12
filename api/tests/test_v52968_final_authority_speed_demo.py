from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def htmls():
    return [(ROOT/'frontend/index.html').read_text(encoding='utf-8'),(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')]

def test_final_authority_is_after_historical_v66_rules():
    for h in htmls():
        assert h.rfind('allroads-v52968-final-authority') > h.rfind('allroads-v52966-landscape-driving-order-test')
        assert h.rfind('allroads-v52968-speed-slider-demo') > h.rfind('allroads-v52968-final-authority')

def test_same_driving_order_is_forced_both_orientations():
    for h in htmls():
        block=h[h.rfind('allroads-v52968-final-authority'):]
        assert '@media (orientation:portrait)' in block
        assert '@media (orientation:landscape)' in block
        assert '.ar525-mapviews' in block and '.ar51-maneuver' in block
        assert 'top:46px!important' in block and 'top:91px!important' in block

def test_speed_demo_white_orange_red_orange_white():
    for h in htmls():
        assert 'const samples=[68,73,75,73,68];' in h
        assert '},5000)}' in h
        assert "r>=1.05?'red':r>=1.03?'orange':'normal'" in h

def test_speed_unit_is_slider_and_persisted():
    for h in htmls():
        assert 'touch-action:none' in h
        assert 'pointerdown' in h and 'pointermove' in h
        assert "localStorage.setItem('allroads-speed-unit',unit)" in h
        assert "k*0.621371" in h

def test_frontend_mirrors_identical():
    assert (ROOT/'frontend/index.html').read_bytes()==(ROOT/'api/frontend/index.html').read_bytes()
