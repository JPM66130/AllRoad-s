from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
BAT=(ROOT/'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8',errors='ignore')
SW=(ROOT/'api/frontend/sw.js').read_text(encoding='utf-8')

def test_version_227():
    assert 'J235 · Virage Serré · Simulation propre · saisie JEPALYS' in HTML
    assert 'V52.9.235' in BAT
    assert 'v=52.9.235&launch=test-terrain-realisable' in BAT
    assert "VERSION='52.9.235'" in SW

def test_same_metric_zoom_for_both_orientations():
    assert 'function metricZoomForHorizon(lat,horizon)' in HTML
    assert 'const referencePixels=650' in HTML
    assert 'let z=metricZoomForHorizon(anchor.lat,horizonMeters);' in HTML
    assert 'if(orientationChanged&&Number.isFinite(arE7LastDrivingCamera?.zoom))z=arE7LastDrivingCamera.zoom;' in HTML

def test_no_destructive_tile_redraw_in_camera_authority():
    block=HTML[HTML.index('function arE7RefreshDrivingTiles()'):HTML.index('let arE7LastDrivingCamera=null;')]
    assert '.redraw()' not in block
    bearing=HTML[HTML.index('function setDrivingBearing(deg)'):HTML.index('function clearDrivingBearing')]
    assert '.redraw()' not in bearing
