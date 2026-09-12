from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
BAT=(ROOT/'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8',errors='ignore')

def test_current_launcher_after_perspective_cleanup():
    assert 'V52.9.235' in BAT
    assert 'v=52.9.235&launch=test-terrain-realisable' in BAT

def test_experimental_perspective_is_fully_removed():
    assert 'ar221-perspective-map' not in HTML
    assert 'maplibre-gl@4.7.1' not in HTML
    assert 'MercatorCoordinate.fromLngLat' not in HTML
    assert 'setFreeCameraOptions' not in HTML

def test_leaflet_single_authority_keeps_real_route_geometry():
    assert 'function focusDrivingRoute(){' in HTML
    assert 'function arE7ApplyDrivingCamera(center,zoom,heading)' in HTML
    assert 'drivingRoutePoints()' in HTML
    assert 'snapToRoute(rawPos,pts,baseZoom)' in HTML
