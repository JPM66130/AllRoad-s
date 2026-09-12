from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
HTML2=(ROOT/'frontend/index.html').read_text(encoding='utf-8')
BAT=(ROOT/'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8')
SW=(ROOT/'api/frontend/sw.js').read_text(encoding='utf-8')

def test_j231_version_and_mirrors():
    assert HTML == HTML2
    assert 'J235 · Virage Serré · Simulation propre · saisie JEPALYS' in HTML
    assert 'V52.9.235' in BAT
    assert 'v=52.9.235&launch=test-terrain-realisable' in BAT
    assert "VERSION='52.9.235'" in SW

def test_route_is_visual_authority():
    assert "className:'ar-driving-route-halo'" in HTML
    assert "className:'ar-driving-route-core'" in HTML
    assert "color:'#0A7BFF'" in HTML
    assert "color:'#003B80'" in HTML
    assert 'arBringDrivingRouteToFront();' in HTML
    assert 'Math.max(6,weight+5)' in HTML

def test_field_camera_is_realistic_not_perspective_experiment():
    assert 'const horizonSeconds=50;' in HTML
    assert 'Math.max(280,speedHorizonMeters,maneuverHorizonMeters)' in HTML
    assert 'usableHeight*0.74' in HTML
    assert 'maplibregl' not in HTML.lower()
