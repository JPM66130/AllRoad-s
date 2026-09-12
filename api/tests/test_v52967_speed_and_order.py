from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend'/'index.html').read_text(encoding='utf-8')

def test_v52967_speed_widget_and_units():
    assert 'id="ar52967-speed"' in HTML
    assert 'data-speed-unit="kmh"' in HTML and 'data-speed-unit="mph"' in HTML
    assert "r>=1.05?'red':r>=1.03?'orange':'normal'" in HTML
    assert "rawKmh==null?'--'" in HTML

def test_v52967_order_both_orientations():
    assert "CONDUITE : ORDRE COMMUN + COMPTEUR VITESSE PERMANENT" in HTML
    assert '#ar-mobile-nav[data-state="driving"] .ar525-mapviews' in HTML
    assert '#ar-mobile-nav[data-state="driving"] .ar51-maneuver' in HTML
    assert 'top:91px!important' in HTML

def test_v52967_gps_and_demo_hooks():
    assert 'window.AllRoadsSpeed67?.setSpeed(value)' in HTML
    assert 'AllRoadsSpeed67.setLimit(Number(e.limit))' in HTML

def test_v52967_mirrors_and_launcher():
    assert HTML==(ROOT/'api'/'frontend'/'index.html').read_text(encoding='utf-8')
    assert (ROOT/'AA_LANCER_JEPALYS.bat').exists()
