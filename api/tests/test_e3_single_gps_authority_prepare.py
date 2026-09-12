from pathlib import Path

ROOT = Path(__file__).parents[2]
HTML = (ROOT / 'api/frontend/index.html').read_text(encoding='utf-8')


def test_native_watch_position_has_one_call_site():
    assert HTML.count('navigator.geolocation.watchPosition(') == 1


def test_prepare_ma_position_uses_e3_runtime_authority():
    start = HTML.index('async function arE7ResolveRoutePoint')
    end = HTML.index('async function previewExisting', start)
    block = HTML[start:end]
    assert 'AllRoadsGpsRuntime.requestFreshPosition' in block
    assert 'getCurrentPosition' not in block
    assert 'vehicleMarker' not in block


def test_runtime_exposes_fresh_position_request():
    assert 'requestFreshPosition: requestFreshReliablePosition' in HTML
    assert 'openNativeGpsWatch' in HTML
