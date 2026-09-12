from pathlib import Path
ROOT = Path(__file__).parents[2]
HTML = (ROOT/'frontend'/'index.html').read_text(encoding='utf-8')
API_HTML = (ROOT/'api'/'frontend'/'index.html').read_text(encoding='utf-8')
LAUNCHER = (ROOT/'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8-sig')

def test_frontends_identical():
    assert HTML == API_HTML

def test_two_visible_views_only_legacy_hidden():
    assert 'html.jepalys-flat #ar52-vehicle{display:none!important}' in HTML
    assert '#ar-mobile-nav[data-state="prepare"] .ar51-state-panel[data-panel="prepare"]' in HTML
    assert '#ar-mobile-nav[data-state="ready"] .ar51-state-panel[data-panel="ready"]' in HTML
    assert 'function installTwoViewGuard()' in HTML
    assert 'showHome()' in HTML

def test_driving_has_single_home_navigation():
    assert '#ar-mobile-nav[data-state="driving"] #ar51-back{display:none!important}' in HTML
    assert '#ar-mobile-nav[data-state="driving"] #ar51-home{display:grid!important' in HTML

def test_real_input_gets_visual_priority_no_clone():
    assert 'body.vsflat-editing input.vsflat-active-input' in HTML
    assert 'position:fixed!important;z-index:10080!important' in HTML
    assert 'function beginEdit(el,opts={})' in HTML
    assert "const clear=el.id==='vsflat-to'" in HTML

def test_tour_is_route_authority_and_has_return():
    assert 'function activeTourData()' in HTML
    assert 'function routeLabel(t)' in HTML
    assert 'function applyTour(t)' in HTML
    assert 'function reverseTour(t)' in HTML
    assert 'data-return=' in HTML
    assert 'Active : ${routeLabel(td)} · gérer' in HTML

def test_home_layout_and_map_recentered():
    assert '.setView([44.4,3.2],6);' in HTML
    assert '.ar-profile-grid{justify-self:center!important;margin-inline:auto!important}' in HTML
    assert 'body.vsflat-panel-open #allroads-mobile-home .ar-home-promo-row' in HTML

def test_launcher_is_single_current_entrypoint():
    bats=list(ROOT.glob('*.bat'))
    assert len(bats)==1 and bats[0].name=='AA_LANCER_JEPALYS.bat'
    assert 'v=52.9.199' in LAUNCHER
