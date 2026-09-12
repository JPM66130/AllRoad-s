from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def text(rel): return (ROOT/rel).read_text(encoding='utf-8')

def test_v82_identity_and_mirrors():
    assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'
    assert 'APP_VERSION = "V52.9.102"' in text('api/main.py')
    assert (ROOT/'AA_LANCER_JEPALYS.bat').exists()
    assert text('frontend/allroads_ui_final.js')==text('api/frontend/allroads_ui_final.js')
    assert text('frontend/allroads_ui_final.css')==text('api/frontend/allroads_ui_final.css')

def test_layout_viewport_is_authority_not_visual_viewport():
    js=text('frontend/allroads_ui_final.js')
    assert 'function layoutSize()' in js
    assert 'window.innerWidth' in js and 'window.innerHeight' in js
    assert "visualViewport.addEventListener('resize'" not in js
    assert 'RECOVERY_DELAY=4000' in js
    assert 'function recoverFrame()' in js
    assert 'scheduleRecovery' in js

def test_mobile_transient_resize_is_ignored_but_desktop_resize_is_supported():
    js=text('frontend/allroads_ui_final.js')
    assert "(standalone()||coarsePointer())&&lastOrientation&&orientation===lastOrientation" in js
    assert 'window.AllRoadsShell61?.recapture' in js

def test_accidental_native_zoom_is_disabled_and_images_are_cropped_inside_frame():
    html=text('frontend/index.html')
    css=text('frontend/allroads_ui_final.css')
    assert 'maximum-scale=1' in html and 'user-scalable=no' in html
    assert 'object-fit:cover!important' in css
    assert 'overscroll-behavior:none' in css
