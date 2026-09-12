from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/"frontend/index.html").read_text(encoding="utf-8")

def test_vehicle_title_is_one_line_without_clipping():
    block=HTML.split('allroads-v52962-wp35-finition',1)[1].split('</style>',1)[0]
    assert 'white-space:nowrap!important' in block
    assert 'font-size:clamp(19px,5.2vw,21px)!important' in block
    assert 'text-overflow:clip!important' in block

def test_native_leaflet_zoom_is_removed_but_allroads_zoom_remains():
    block=HTML.split('allroads-v52962-wp35-finition',1)[1].split('</style>',1)[0]
    assert '#ar-mobile-nav .leaflet-control-zoom{display:none!important}' in block
    assert 'id="ar51-zoom-in"' in HTML and 'id="ar51-zoom-out"' in HTML

def test_single_shell_authority_ignores_same_orientation_resize():
    block=HTML.split('allroads-v52962-single-shell-authority',1)[1].split('</script>',1)[0]
    assert "if(orient(w,h)===currentOrientation) return" in block
    assert "window.addEventListener('resize',onResize" in block
    legacy59=HTML.split('allroads-v52959-fixed-shell-js',1)[1].split('</script>',1)[0]
    legacy60=HTML.split('allroads-v52960-android-bars-stability',1)[1].split('</script>',1)[0]
    assert "addEventListener('resize'" not in legacy59
    assert "addEventListener('resize'" not in legacy60
    assert block.count("window.addEventListener('resize'") == 1
    assert HTML.count("visualViewport.addEventListener('resize'") == 1
