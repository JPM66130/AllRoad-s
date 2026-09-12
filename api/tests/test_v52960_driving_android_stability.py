from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend'/'index.html').read_text(encoding='utf-8')

def test_driving_mapviews_are_above_maneuver():
    assert 'allroads-v52960-driving-order' in HTML
    block=HTML.split('allroads-v52960-driving-order',1)[1].split('</style>',1)[0]
    assert '[data-state="driving"] .ar525-mapviews' in block
    assert '[data-state="driving"] .ar51-maneuver' in block
    assert 'z-index:460!important' in block
    assert 'z-index:450!important' in block

def test_android_bar_resize_never_shrinks_shell():
    assert 'allroads-v52960-android-bars-stability' in HTML
    block=HTML.split('allroads-v52960-android-bars-stability',1)[1].split('</script>',1)[0]
    assert 'if(w>maxW || h>maxH)' in block
    assert 'Math.max(maxW,w)' in block and 'Math.max(maxH,h)' in block
    # visualViewport resize remains reserved to keyboard controller only.
    assert HTML.count("visualViewport.addEventListener('resize'") == 1
