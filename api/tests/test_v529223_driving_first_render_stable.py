from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
HTML2=(ROOT/'frontend/index.html').read_text(encoding='utf-8')
LAUNCH=(ROOT/'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8')

def test_frontends_identical():
    assert HTML == HTML2

def test_single_stabilizer_exists():
    assert 'function ar223StabilizeDrivingCamera' in HTML
    assert "stabilize?.('enter-driving')" in HTML
    assert "stabilize?.('orientationchange')" in HTML

def test_stabilizer_remeasures_before_camera():
    body=HTML.split('function ar223StabilizeDrivingCamera',1)[1].split('window.AllRoadsCamera223',1)[0]
    assert 'map.invalidateSize' in body
    assert 'arE7RefreshDrivingTiles' in body
    assert 'focusDrivingRoute' in body

def test_launcher_bumped():
    assert '52.9.235' in LAUNCH
