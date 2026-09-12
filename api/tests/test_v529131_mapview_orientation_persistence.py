from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "frontend" / "index.html"

def test_driving_base_layer_uses_selected_view_not_fixed_drive_layer():
    s = HTML.read_text(encoding="utf-8")
    assert "function arDrivingSelectedViewName()" in s
    assert "const wantedName=arDrivingSelectedViewName();" in s
    assert "mapViews.drive.addTo(map);activeMapView=mapViews.drive;" not in s

def test_selected_view_persists_from_mobile_choice():
    s = HTML.read_text(encoding="utf-8")
    assert "allroads-v525-mobile-map-view" in s
    assert "['normal','complex','satellite'].includes(stored)" in s
