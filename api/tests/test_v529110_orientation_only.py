from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / 'frontend' / 'index.html'
TEXT = HTML.read_text(encoding='utf-8')


def test_v529118_real_map_size_driver_anchor_present():
    assert 'const size=map.getSize();' in TEXT
    assert 'let targetY=Math.round(usableTop+usableHeight*0.74);' in TEXT
    assert 'const targetX=Math.round(size.x*0.50);' in TEXT
    assert 'const centerPx=L.point(pa.x-preRot.x,pa.y-preRot.y);' in TEXT
    assert 'arE7ApplyDrivingCamera(map.unproject(centerPx,z),z,heading);' in TEXT


def test_v529118_does_not_place_vehicle_or_change_gps_logic():
    block = TEXT.split('function focusDrivingRoute(){',1)[1].split('let recenterTimer=',1)[0]
    assert 'gpsSpeed' not in block
    assert '#ar5268-drive-vehicle{display:none!important}' in TEXT


def test_v529118_frontend_mirrors_match():
    root = Path(__file__).resolve().parents[2]
    a = (root / 'api' / 'frontend' / 'index.html').read_bytes()
    b = (root / 'frontend' / 'index.html').read_bytes()
    assert a == b
