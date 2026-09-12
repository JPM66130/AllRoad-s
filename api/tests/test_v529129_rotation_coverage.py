from pathlib import Path

HTML=(Path(__file__).resolve().parents[1]/"frontend"/"index.html").read_text(encoding="utf-8")

def test_rotation_cover_scale_is_geometric_and_not_constant():
    assert "function arE7RotationCoverScale(deg,size=map.getSize())" in HTML
    assert "(w*c+h*s)/w" in HTML
    assert "(w*s+h*c)/h" in HTML
    assert "scale(1.18)" not in HTML

def test_camera_center_compensates_rotation_cover_scale():
    b=HTML.split("function focusDrivingRoute(){",1)[1].split("let recenterTimer=",1)[0]
    assert "const coverScale=arE7RotationCoverScale(heading,size);" in b
    assert "/coverScale" in b
    assert "rx*coverScale" in b and "ry*coverScale" in b
    assert "arE7ApplyDrivingCamera(map.unproject(centerPx,z),z,heading);" in b

def test_cover_scale_applies_to_all_leaflet_visual_panes():
    b=HTML.split("function setDrivingBearing(deg){",1)[1].split("function clearDrivingBearing()",1)[0]
    assert ".leaflet-tile-pane,.leaflet-overlay-pane,.leaflet-shadow-pane,.leaflet-marker-pane,.leaflet-tooltip-pane,.leaflet-popup-pane" in HTML
    assert "rotate(${-normalized}deg) scale(${scale})" in b
