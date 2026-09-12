from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CSS=(ROOT/'frontend'/'allroads_ui_final.css').read_text(encoding='utf-8')
JS=(ROOT/'frontend'/'allroads_ui_final.js').read_text(encoding='utf-8')
HTML=(ROOT/'frontend'/'index.html').read_text(encoding='utf-8')

def test_version_and_authority():
    assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'
    assert 'allroads_ui_final.css?v=52.9.91' in HTML
    assert 'allroads_ui_final.js?v=52.9.91' in HTML

def test_screen_adapter_uses_real_viewport():
    assert 'visualViewport' in JS
    assert 'data-ar-size' in CSS
    assert "docEl.dataset.arSize=size" in JS
    assert "docEl.dataset.arOrientation" in JS
    assert "--ar-screen-w" in JS and "--ar-screen-h" in JS

def test_theme_switch_has_touch_priority():
    assert 'z-index:2147483000!important' in CSS
    assert 'pointer-events:auto!important' in CSS
    assert 'stopImmediatePropagation' in JS
    assert 'capture:true' in JS

def test_prepare_gives_more_room_to_route_fields():
    assert 'minmax(410px,2.28fr)' in CSS
    assert 'minmax(205px,.78fr)' in CSS

def test_mirrors_match():
    for f in ['allroads_ui_final.css','allroads_ui_final.js','index.html','sw.js','manifest.webmanifest']:
        assert (ROOT/'frontend'/f).read_bytes()==(ROOT/'api'/'frontend'/f).read_bytes()
