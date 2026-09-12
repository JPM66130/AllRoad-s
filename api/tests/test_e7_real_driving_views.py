from pathlib import Path
HTML = Path('api/frontend/index.html').read_text(encoding='utf-8')

def test_single_camera_authority_replaces_persisted_overhead_mode():
    assert "const arE7CameraMode='driver'" in HTML
    assert "authority:'single'" in HTML
    assert "localStorage.getItem('allroads-e7-camera')" not in HTML
    assert "#ar-e7-camera-toggle{display:none!important}" in HTML

def test_visual_brick_owns_demo_without_legacy_demo_class():
    block=HTML.split('id="allroads-e7-visual-brick-js"',1)[1]
    assert "b.dataset.arVisualMode=mode;" in block
    assert "b.classList.remove('ar52620-demo-camera','ar5289-prades-vernet');" in block
    assert "classList.toggle('ar52620-demo-camera'" not in block

def test_real_start_still_starts_single_gps_runtime():
    assert "const started=window.AllRoadsGpsRuntime?.start();" in HTML
    assert HTML.count('navigator.geolocation.watchPosition(') == 1
