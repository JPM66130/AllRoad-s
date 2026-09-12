from pathlib import Path

HTML = (Path(__file__).parents[1] / 'frontend' / 'index.html').read_text(encoding='utf-8')

def test_v5265_camera_keeps_route_and_vehicle_in_same_rotated_geometry():
    assert 'ar5265-bearing-up .leaflet-marker-pane' in HTML
    assert 'ar5265-bearing-up .leaflet-overlay-pane' in HTML
    assert '--ar-vehicle-counter-rotation' in HTML
    assert 'const z=17;' in HTML
    assert 'syncMobileDriveMarker();' in HTML
