from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
HTML2=(ROOT/'frontend/index.html').read_text(encoding='utf-8')
BAT=(ROOT/'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8')
SW=(ROOT/'api/frontend/sw.js').read_text(encoding='utf-8')

def test_version_226():
    assert 'J235 · Virage Serré · Simulation propre · saisie JEPALYS' in HTML
    assert 'V52.9.235' in BAT
    assert 'v=52.9.235&launch=test-terrain-realisable' in BAT
    assert "VERSION='52.9.235'" in SW

def test_orientation_has_no_freeze_clone_or_mask():
    assert 'ar222-orientation-freeze' not in HTML
    assert 'ar222FreezeMapFrame' not in HTML
    assert 'cloneNode(true)' not in HTML[HTML.index('allroads-v529226-camera-cleanup'):]
    assert 'AllRoadsCamera226' in HTML

def test_leaflet_fades_disabled_for_rotation_stability():
    assert 'fadeAnimation:false' in HTML
    assert 'zoomAnimation:false' in HTML
    assert 'markerZoomAnimation:false' in HTML

def test_frontends_identical():
    assert HTML == HTML2
