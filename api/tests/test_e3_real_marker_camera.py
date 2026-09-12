from pathlib import Path

HTML = Path('api/frontend/index.html').read_text(encoding='utf-8')


def _sync_block():
    start = HTML.index('function syncMobileDriveMarker()')
    end = HTML.index('function drawDemo()', start)
    return HTML[start:end]


def test_real_marker_uses_gps_as_only_position_authority():
    block = _sync_block()
    assert 'const gpsPos=arE7FreshRealGpsLatLng();' in block
    assert 'vehicleMarker' not in block
    assert 'mobileDriveMarker=makeNeutralVehicleMarker(gpsPos);' in block
    assert 'const pts=drivingRoutePoints();' not in block
    assert 'pts[0]' not in block


def test_real_marker_is_not_invented_before_first_gps_fix():
    block = _sync_block()
    assert 'if(!gpsPos)return;' in block
    assert 'if(!mobileDriveMarker)mobileDriveMarker=makeNeutralVehicleMarker(gpsPos);' in block
    assert 'else mobileDriveMarker.setLatLng(gpsPos);' in block


def test_each_reliable_gps_fix_updates_marker_before_camera_focus():
    gps_update = HTML.index('if (mobileDriveMarker) mobileDriveMarker.setLatLng(currentPos);')
    camera_focus = HTML.index("if ((document.getElementById('ar-mobile-nav')?.dataset?.state||'') === 'driving') focusDrivingRoute();", gps_update)
    assert gps_update < camera_focus
