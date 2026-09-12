from pathlib import Path

ROOT=Path(__file__).parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')

def test_camera_uses_explicit_fresh_reliable_gps_authority():
    assert 'window.__allroadsReliableGpsFix = {' in HTML
    assert 'if(Date.now()-f.at>15000)return null;' in HTML
    focus=HTML.split('function focusDrivingRoute(){',1)[1].split('let recenterTimer=',1)[0]
    assert "const rawPos=demoMode ? (arJ232SimPos||demoMarker?.getLatLng?.()) : arE7FreshRealGpsLatLng();" in focus
    assert 'mobileDriveMarker?.getLatLng?.()' not in focus
    assert 'arJ232SimPos' in focus

def test_old_mobile_marker_is_cleared_when_real_driving_starts():
    start=HTML.split('function startDriving(){',1)[1].split('function open(p)',1)[0]
    assert 'mobileDriveMarker=null;' in start
    assert "window.AllRoadsGpsRuntime?.start()" in start

def test_camera_diagnostic_exposes_waiting_applied_error_states():
    assert 'window.AllRoadsCameraAuthority={' in HTML
    assert "arE7CameraDiag(!rawPos?'waiting-gps':'waiting-route'" in HTML
    assert "arE7CameraDiag('applied'" in HTML
    assert "arE7CameraDiag('error'" in HTML

def test_frontend_mirrors_identical():
    assert (ROOT/'frontend/index.html').read_bytes()==(ROOT/'api/frontend/index.html').read_bytes()
