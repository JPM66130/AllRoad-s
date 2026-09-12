from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend'/'index.html').read_text(encoding='utf-8')

def test_version_52940_visible():
    assert 'V52.9.102' in HTML

def test_home_has_true_landscape_4x2_standard():
    assert 'ACCUEIL SIGNATURE PAYSAGE' in HTML
    assert 'grid-template-columns:repeat(4,minmax(0,1fr))!important' in HTML
    assert 'grid-template-rows:repeat(2,minmax(0,1fr))!important' in HTML

def test_home_orientation_does_not_switch_screen():
    assert 'body.ar-mobile-home-open #allroads-mobile-home.ar-home' in HTML
    assert 'display:flex!important' in HTML

def test_ready_panel_is_compact_in_landscape():
    assert '#ar-mobile-nav[data-state="ready"] .ar51-sheet' in HTML
    assert 'height:88px!important;max-height:88px!important' in HTML

def test_standard_panel_tokens_exist():
    for token in ('--ar-panel-radius:15px','--ar-panel-gap:7px','--ar-action-h:42px','--ar-action-radius:12px'):
        assert token in HTML

def test_ready_information_and_actions_stay_present():
    for token in ('Itinéraire prêt','id="ar51-ready-dest"','id="ar51-km"','id="ar51-min"','Alerte critique','id="ar51-start"','id="ar51-edit"'):
        assert token in HTML
