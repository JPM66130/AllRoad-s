from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
LAUNCHER=(ROOT/'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8')

def test_launcher_226():
    assert 'V52.9.235' in LAUNCHER
    assert 'v=52.9.235&launch=test-terrain-realisable' in LAUNCHER

def test_removed_perspective_and_orientation_ghosts():
    assert 'ar221-perspective-map' not in HTML
    assert 'data-ar221-maplibre' not in HTML
    assert 'ar222-orientation-freeze' not in HTML
    assert 'ar222FreezeMapFrame' not in HTML

def test_single_camera_authority():
    assert "const arE7CameraMode='driver'" in HTML
    assert "getState:()=>({mode:'driver',authority:'single'})" in HTML
    assert 'AllRoadsCamera226' in HTML
    assert 'focusDrivingRoute() / arE7ApplyDrivingCamera()' in HTML

def test_old_camera_classes_not_manipulated():
    assert 'ar5265-bearing-up' not in HTML
    assert 'ar5266-driving-camera' not in HTML
    assert 'ar5267-driving-camera' not in HTML
