from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CSS=(ROOT/'frontend'/'allroads_ui_final.css').read_text(encoding='utf-8')
JS=(ROOT/'frontend'/'allroads_ui_final.js').read_text(encoding='utf-8')
HTML=(ROOT/'frontend'/'index.html').read_text(encoding='utf-8')

def test_version_and_authority():
    assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'
    assert 'allroads_ui_final.css?v=52.9.91' in HTML
    assert 'allroads_ui_final.js?v=52.9.91' in HTML

def test_prepare_ready_share_landscape_shell():
    assert 'height:76px!important' in CSS
    assert '#ar-mobile-nav[data-state="prepare"] .ar51-sheet' in CSS
    assert '#ar-mobile-nav[data-state="ready"] .ar51-sheet' in CSS
    assert 'display:contents!important' in CSS
    assert 'grid-template-columns:minmax(165px,.9fr) minmax(340px,1.8fr) minmax(260px,1.15fr)' in CSS

def test_demo_without_gps_remains_present():
    assert 'id="ar51-demo"' in HTML
    assert 'Démo sans GPS' in HTML

def test_portrait_theme_controls_do_not_overlap():
    assert 'width:190px!important;max-width:190px!important' in CSS
    assert 'right:62px!important;width:118px!important;height:27px!important' in CSS

def test_night_keeps_scene_visible():
    assert 'body.ar-night #ar-mobile-nav{background:transparent!important}' in CSS
    assert 'background:rgba(2,12,24,.12)' in CSS
    assert '#ar5296-drive-canvas' in CSS and 'filter:none!important' in CSS

def test_vehicle_check_moves_to_actions():
    assert 'normalizeVehicleSelection' in JS
    assert "actions.appendChild(check)" in JS
    assert '.ar52-card-actions .ar52-selected-check{position:static!important' in CSS
