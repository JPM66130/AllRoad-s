from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSS = (ROOT/'frontend'/'allroads_ui_final.css').read_text(encoding='utf-8')
JS = (ROOT/'frontend'/'allroads_ui_final.js').read_text(encoding='utf-8')
HTML = (ROOT/'frontend'/'index.html').read_text(encoding='utf-8')
SW = (ROOT/'frontend'/'sw.js').read_text(encoding='utf-8')


def test_version_78_everywhere():
    assert 'V52.9.102' in (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8')
    assert 'V52.9.102' in (ROOT/'api'/'main.py').read_text(encoding='utf-8')
    assert 'allroads_ui_final.css?v=52.9.91' in HTML
    assert 'allroads_ui_final.js?v=52.9.91' in HTML
    assert "const VERSION='52.9.97'" in SW


def test_night_never_masks_the_whole_navigation_root():
    assert 'body.ar-night #ar-mobile-nav{background:transparent!important}' in CSS
    assert 'body.ar-night #ar-mobile-nav{background:#07111d!important}' not in CSS
    assert 'background:rgba(2,12,24,.12)' in CSS


def test_canvas_is_kept_visible_in_driving_states():
    assert '#ar-mobile-nav[data-state="driving"] #ar5296-drive-canvas' in CSS
    assert 'display:block!important;visibility:visible!important;opacity:1!important;filter:none!important' in CSS


def test_portrait_maneuver_is_compact_single_line():
    assert 'height:58px!important;min-height:58px!important' in CSS
    assert '.ar51-step{display:flex!important;align-items:center!important' in CSS
    assert 'white-space:nowrap!important' in CSS


def test_landscape_prepare_and_ready_share_one_height():
    assert '#ar-mobile-nav[data-state="prepare"] .ar51-sheet,\n  #ar-mobile-nav[data-state="ready"] .ar51-sheet' in CSS
    assert 'height:76px!important;min-height:76px!important;max-height:76px!important' in CSS


def test_vehicle_has_single_profile_indicator_authority():
    assert 'body.ar52-vehicle-open .ar-standard-context{display:none!important}' in CSS
    assert 'body.ar52-vehicle-open .ar52-profile::before' in CSS


def test_frontend_mirrors_are_identical():
    for name in ['index.html','allroads_ui_final.css','allroads_ui_final.js','sw.js','manifest.webmanifest']:
        assert (ROOT/'frontend'/name).read_bytes() == (ROOT/'api'/'frontend'/name).read_bytes()
