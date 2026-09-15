from pathlib import Path

HTML = (Path(__file__).parents[1] / 'frontend' / 'index.html').read_text(encoding='utf-8')


def _focus_block():
    return HTML.split('function focusDrivingRoute(){', 1)[1].split('let recenterTimer=', 1)[0]


def test_real_driver_camera_rotates_leaflet_panes_with_calculated_cover_scale():
    assert "function arE7RotationCoverScale(deg,size=map.getSize())" in HTML
    assert "p.style.transform=`rotate(${-normalized}deg) scale(${scale})`" in HTML
    assert "scale(1.18)" not in HTML


def test_v529118_keeps_route_heading_orientation_with_single_apply_path():
    block = _focus_block()
    assert 'const headingPoint=pointAtDistance' in block
    assert 'const rawHeading=Math.atan2(headingDx,-headingDy)*180/Math.PI;' in block
    assert 'heading=previousHeading+delta*0.22;' in block
    assert 'arE7ApplyDrivingCamera(map.unproject(centerPx,z),z,heading);' in block
    assert 'lookAheadPx' not in block
    assert 'cameraCenter' not in block


def test_v529117_zoom_is_calculated_from_viewport_and_route():
    block = _focus_block()
    assert 'const baseZoom=map.getZoom();' in block
    assert 'const farZoom=harmonizedFarZoom(anchor.lat);' in block
    assert 'ar221RefreshPerspective' not in block
    assert 'arE7ApplyDrivingCamera' in block
    assert 'const exactZoom=referenceZoom+Math.log2(scaleLimit);' in block
    assert 'Math.floor(exactZoom*4)/4' in block
    assert 'horizonMeters' in block
    assert 'gpsSpeed' not in block
    assert 'map.panBy(' not in block


def test_v529112_vehicle_stays_hidden_until_stage_three():
    assert '#ar5268-drive-vehicle{display:none!important}' in HTML
    assert '#map .ar5263-vehicle-icon{opacity:0!important}' in HTML
