from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend/index.html').read_text(encoding='utf-8')

def block(): return HTML.split('function focusDrivingRoute(){',1)[1].split('let recenterTimer=',1)[0]

def test_zoom_uses_rotated_forward_route_bounds():
    b=block()
    assert 'function forwardRouteSample()' in b
    assert 'const referenceZoom=16;' in b
    assert 'scaleLimit=Math.min' in b
    assert 'const exactZoom=referenceZoom+Math.log2(scaleLimit);' in b

def test_same_heading_drives_rotation_and_fit_geometry():
    b=block()
    assert 'const theta=heading*Math.PI/180;' in b
    assert 'const rx=vx*Math.cos(theta)+vy*Math.sin(theta);' in b
    assert 'const preRot=L.point(' in b
    assert 'arE7ApplyDrivingCamera(map.unproject(centerPx,z),z,heading);' in b

def test_no_manual_pixel_pan_or_relative_zoom():
    b=block()
    assert 'map.panBy(' not in b
    assert 'baseZoom+1' not in b and 'baseZoom+2' not in b

def test_frontend_mirrors_match():
    assert (ROOT/'frontend/index.html').read_bytes()==(ROOT/'api/frontend/index.html').read_bytes()
