from pathlib import Path

HTML=Path("api/frontend/index.html").read_text(encoding="utf-8")

def block():
    return HTML.split("function focusDrivingRoute(){",1)[1].split("let recenterTimer=",1)[0]

def test_usable_map_rectangle_is_measured_from_real_dom():
    b=block()
    assert "function mapLocalRect(node)" in b
    assert "getBoundingClientRect" in b
    assert "const usableTop=Math.max(...topCandidates);" in b
    assert "const usableBottom=Math.max(usableTop+180,size.y-bottomReserve);" in b

def test_driver_anchor_is_relative_to_usable_rectangle():
    b=block()
    assert "const targetX=Math.round(size.x*0.50);" in b
    assert "let targetY=Math.round(usableTop+usableHeight*0.74);" in b

def test_leaflet_center_is_exact_inverse_rotation_solution():
    b=block()
    assert "const desired=L.point(targetX-screenCenter.x,targetY-screenCenter.y);" in b
    assert "const preRot=L.point(" in b
    assert "const centerPx=L.point(pa.x-preRot.x,pa.y-preRot.y);" in b
    assert "arE7ApplyDrivingCamera(map.unproject(centerPx,z),z,heading);" in b

def test_camera_diagnostic_reports_geometry():
    b=block()
    for token in ["targetX,targetY","usableTop:Math.round(usableTop)","usableBottom:Math.round(usableBottom)","usableHeight:Math.round(usableHeight)"]:
        assert token in b
