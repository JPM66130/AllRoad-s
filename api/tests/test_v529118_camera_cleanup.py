from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend/index.html').read_text(encoding='utf-8')
API_HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
SW=(ROOT/'frontend/sw.js').read_text(encoding='utf-8')

def camera_block():
    return HTML.split('function focusDrivingRoute(){',1)[1].split('let recenterTimer=',1)[0]

def test_no_arbitrary_hidden_scale_in_driving_bearing():
    bearing=HTML.split('function setDrivingBearing(deg){',1)[1].split('function clearDrivingBearing()',1)[0]
    assert 'scale(1.18)' not in bearing
    assert 'const scale=arE7RotationCoverScale(normalized,size);' in bearing
    assert 'rotate(${-normalized}deg) scale(${scale})' in bearing

def test_single_camera_apply_path_and_clean_measurement():
    b=camera_block()
    assert 'arE7ResetDrivingPaneTransform();' in b
    assert 'arE7ApplyDrivingCamera(map.unproject(centerPx,z),z,heading);' in b
    assert 'map.setView(map.unproject(centerPx,z)' not in b

def test_local_axis_drives_center_and_orientation():
    b=camera_block()
    assert 'const headingPoint=pointAtDistance' in b
    assert 'const headingProbeA=map.project(anchor,15),headingProbeB=map.project(headingPoint,15);' in b
    assert 'const pa=map.project(anchor,z);' in b
    assert 'const centerPx=L.point(pa.x-preRot.x,pa.y-preRot.y);' in b
    assert 'const heading=Math.atan2(headingDx,-headingDy)*180/Math.PI;' in b

def test_no_route_start_as_fake_driver_anchor_without_gps():
    b=camera_block()
    assert 'if(!rawPos||pts.length<2)' in b
    assert 'let i=0,anchor=pts[0]' not in b

def test_sw_version_aligned_and_frontends_match():
    assert HTML == API_HTML
