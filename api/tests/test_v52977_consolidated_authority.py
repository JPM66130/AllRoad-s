from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def text(p): return (ROOT/p).read_text(encoding='utf-8')

def test_version_and_single_authority_assets():
    assert 'V52.9.102' in text('api/main.py')
    assert text('VERSION_DEMO.txt').strip()=='V52.9.102'
    h=text('frontend/index.html')
    assert 'allroads_ui_final.css?v=52.9.91' in h
    assert 'allroads_ui_final.js?v=52.9.91' in h
    assert 'allroads-v52969-shell-candidate' not in h
    assert 'allroads-v52976-three-fixes' not in h

def test_mirrors_identical():
    for f in ['index.html','allroads_ui_final.css','allroads_ui_final.js','sw.js','manifest.webmanifest']:
        assert (ROOT/'frontend'/f).read_bytes()==(ROOT/'api/frontend'/f).read_bytes()

def test_night_is_overlay_not_canvas_filter():
    css=text('frontend/allroads_ui_final.css')
    js=text('frontend/allroads_ui_final.js')
    assert '#ar52977-night-overlay' in css
    assert 'body.ar-night #ar52977-night-overlay{display:block!important}' in css
    assert 'filter:none!important' in css
    assert "document.body.classList.toggle('ar-night',night)" in js
    assert "map.appendChild(o)" in js

def test_portrait_maneuver_and_scene_authority():
    css=text('frontend/allroads_ui_final.css')
    assert 'grid-template-columns:42px minmax(0,1fr) 42px' in css
    assert 'white-space:nowrap!important' in css
    assert '#ar-mobile-nav[data-state="driving"] #ar5296-drive-canvas' in css

def test_prepare_only_button_height_compacted():
    css=text('frontend/allroads_ui_final.css')
    assert '#ar-mobile-nav[data-state="prepare"] .ar526-prepare-actions button{height:43px!important' in css
