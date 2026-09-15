from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
LAUNCHER=(ROOT/'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8')
SW=(ROOT/'api/frontend/sw.js').read_text(encoding='utf-8')

def test_v215_version_and_launch_token():
    assert 'J235 · Virage Serré · Simulation propre · saisie JEPALYS' in HTML
    assert 'V52.9.235' in LAUNCHER
    assert 'v=52.9.235&launch=test-terrain-realisable' in LAUNCHER
    assert "VERSION='52.9.235'" in SW

def test_v215_camera_uses_fractional_geometry_not_manual_zoom_delta():
    assert 'map.options.zoomSnap=0.25;map.options.zoomDelta=0.25;' in HTML
    assert 'const headingPoint=pointAtDistance(Math.min(420,Math.max(140,horizonMeters*.18)));' in HTML
    assert 'const localManeuverCeiling=Math.max(500,Math.min(1200,speedHorizonMeters*1.35||500));' in HTML
    assert 'const desiredHorizonMeters=Math.min(1800,Math.max(280,Number.isFinite(maneuverMeters)?Math.min(speedHorizonMeters||280,Math.max(280,maneuverMeters*1.10)):speedHorizonMeters||280));' in HTML
    assert 'const exactZoom=referenceZoom+Math.log2(scaleLimit);' in HTML
    assert 'Math.floor(exactZoom*4)/4' in HTML
    assert 'for(let candidate=11;candidate<=17;candidate++)' not in HTML

def test_v215_keeps_single_camera_application_authority():
    assert 'arE7ApplyDrivingCamera(map.unproject(centerPx,z),z,heading);' in HTML
    assert 'let targetY=Math.round(usableTop+usableHeight*0.74);' in HTML
