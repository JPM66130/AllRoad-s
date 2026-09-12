from pathlib import Path

ROOT=Path(__file__).parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')

def test_demo_calculates_real_route_before_simulation():
    block=HTML.split('async function demoDirect',1)[1].split('window.AllRoadsMobileNav=',1)[0]
    assert 'await previewExisting()' in block
    assert "allroads:route-ready" in block
    assert 'drawDemo()' not in block
    assert 'demoMode=true' in block

def test_simulation_interpolates_on_real_route_geometry():
    assert 'function arJ232BuildRouteSimulation()' in HTML
    assert 'const pts=layerRoutePoints(routeLayer);' in HTML
    assert 'function arJ232PointAtDistance(targetM)' in HTML
    assert 'arJ232SimTotalM+=pts[i-1].distanceTo(pts[i])' in HTML
    assert 'arJ232SimDurationMs=routeMin*60000' in HTML

def test_simulation_position_is_explicit_camera_authority():
    focus=HTML.split('function focusDrivingRoute(){',1)[1].split('let recenterTimer=',1)[0]
    assert "const rawPos=demoMode ? (arJ232SimPos||demoMarker?.getLatLng?.()) : arE7FreshRealGpsLatLng();" in focus
    assert 'arJ232SimPos=pos' in HTML

def test_demo_stops_real_gps_and_does_not_start_legacy_fake_speed():
    start=HTML.split('function startDriving(){',1)[1].split('function open(p)',1)[0]
    assert "window.AllRoadsGpsRuntime?.stop('switch-to-simulation')" in start
    assert 'arJ232StartRouteSimulation()' in start
    assert 'ar52967StartDemoSpeed()' not in start
    assert 'ar5287Start' not in start

def test_frontend_mirrors_identical_j232():
    assert (ROOT/'frontend/index.html').read_bytes()==(ROOT/'api/frontend/index.html').read_bytes()
