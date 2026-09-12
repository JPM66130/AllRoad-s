from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / 'frontend' / 'index.html'
TEXT = HTML.read_text(encoding='utf-8')


def test_v529117_zoom_depends_on_real_map_size_and_route_geometry():
    block = TEXT.split('function focusDrivingRoute(){', 1)[1].split('let recenterTimer=', 1)[0]
    assert 'const size=map.getSize();' in block
    assert 'let targetY=Math.round(usableTop+usableHeight*0.74);' in block
    assert 'const targetTopY=Math.round(usableTop+usableHeight*0.10);' in block
    assert 'const farZoom=harmonizedFarZoom(anchor.lat);' in block
    assert 'ar221RefreshPerspective' not in block
    assert 'arE7ApplyDrivingCamera' in block
    # V52.9.124 conserve le principe de zoom géométrique de 117, mais l'horizon
    # est désormais dérivé de la vitesse et borné au lieu d'être une fraction
    # du trajet restant.
    assert 'const horizonMeters=' in block
    assert 'const exactZoom=referenceZoom+Math.log2(scaleLimit);' in block
    assert 'Math.floor(exactZoom*4)/4' in block


def test_v529117_no_manual_relative_zoom_choice_or_gps_change():
    block = TEXT.split('function focusDrivingRoute(){', 1)[1].split('let recenterTimer=', 1)[0]
    assert 'baseZoom+1' not in block
    assert 'baseZoom+2' not in block
    assert 'gpsSpeed' not in block
    assert '#ar5268-drive-vehicle{display:none!important}' in TEXT


def test_v529117_frontend_mirrors_match():
    root = Path(__file__).resolve().parents[2]
    assert (root / 'api' / 'frontend' / 'index.html').read_bytes() == (root / 'frontend' / 'index.html').read_bytes()
