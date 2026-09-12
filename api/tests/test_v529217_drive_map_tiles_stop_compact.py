from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
LAUNCHER=(ROOT/'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8')

def test_v217_identity():
    assert 'J235 · Virage Serré · Simulation propre · saisie JEPALYS' in HTML
    assert 'V52.9.235' in LAUNCHER
    assert 'v=52.9.235&launch=test-terrain-realisable' in LAUNCHER

def test_drive_tiles_are_refreshed_after_camera_and_orientation():
    assert 'function arE7RefreshDrivingTiles()' in HTML
    assert "function arE7RefreshDrivingTiles()" in HTML
    refresh=HTML[HTML.index('function arE7RefreshDrivingTiles()'):HTML.index('let arE7LastDrivingCamera=null;')]
    assert '.redraw()' not in refresh
    apply=HTML[HTML.index('function arE7ApplyDrivingCamera'):HTML.index('function arE7RotationCoverScale')]
    assert 'requestAnimationFrame(()=>arE7RefreshDrivingTiles())' not in apply
    assert "stabilize?.('orientationchange')" in HTML

def test_bus_stop_floating_is_compact():
    assert 'width:60px!important;min-width:60px!important;max-width:60px!important;height:60px!important' in HTML
    assert 'font-size:12px!important;z-index:9750!important' in HTML
