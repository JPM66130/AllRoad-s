from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
TEXT = HTML.read_text(encoding="utf-8")

def test_v529111_rotation_uses_visual_center():
    assert "cx=mr.left+mr.width/2,cy=mr.top+mr.height/2" in TEXT
    assert "cy=mr.top+mr.height*.72" not in TEXT

def test_v529111_keeps_orientation_only_scope():
    block = TEXT.split("function focusDrivingRoute(){",1)[1].split("let recenterTimer=",1)[0]
    assert "map.setView(cameraCenter" not in block
    assert "map.panBy(" not in block
    assert "lookAheadPx" not in block
    assert "arE7ApplyDrivingCamera(map.unproject(centerPx,z),z,heading);" in block
