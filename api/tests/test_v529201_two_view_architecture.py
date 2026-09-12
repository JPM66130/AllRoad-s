from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend/index.html').read_text(encoding='utf-8')
SOUP=BeautifulSoup(HTML,'html.parser')
LAUNCHER=(ROOT/'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8-sig')


def test_only_two_primary_user_views_remain():
    assert SOUP.find(id='allroads-mobile-home') is not None
    assert SOUP.find(id='ar-mobile-nav') is not None
    assert SOUP.find(id='ar52-vehicle') is None
    assert SOUP.select_one('.ar51-state-panel[data-panel="prepare"]') is None
    assert SOUP.select_one('.ar51-state-panel[data-panel="ready"]') is None


def test_legacy_route_state_is_engine_only_not_page():
    engine=SOUP.find(id='ar-route-engine-state')
    assert engine is not None
    assert engine.has_attr('hidden')
    assert engine.find(id='ar51-from') is not None
    assert engine.find(id='ar51-to') is not None


def test_profile_selection_no_longer_opens_legacy_nav():
    start=HTML.index('function continueWithProfile()')
    end=HTML.index('window.addEventListener("load"',start)
    block=HTML[start:end]
    assert 'AllRoadsMobileNav.open' not in block
    assert 'openHome()' in block


def test_legacy_open_is_nonvisual_adapter():
    start=HTML.index('function open(p)')
    end=HTML.index('function close()',start)
    block=HTML[start:end]
    assert "classList.add('ar-mobile-nav-open')" not in block
    assert "n.style.display='none'" in block
    assert "classList.add('ar-mobile-home-open')" in block


def test_route_calculation_is_headless_then_direct_drive():
    assert 'compareHeadless?.(v.p,v.from,v.to,prefs)' in HTML
    assert 'calculateHeadless?.(ctx.v.p,ctx.v.from,ctx.v.to' in HTML
    assert "window.addEventListener('allroads:route-ready',()=>{if(!autoStart)return;autoStart=false;resetRouteButton();startDrive()})" in HTML


def test_manual_destination_returns_origin_to_my_position():
    assert "const f=by('vsflat-from');if(f)f.value='Ma position'" in HTML
    assert "if(activeTour())setActiveTour(null,false)" in HTML


def test_tour_label_and_return_share_same_endpoints():
    assert "return e.to?`${e.from} - ${e.to}`:e.from" in HTML
    assert "from:e.to||'',to:e.from||'Ma position'" in HTML
    assert "stops:Array.isArray(t.stops)?[...t.stops].reverse():[]" in HTML


def test_single_input_authority_after_cleanup():
    assert 'allroads-v52951-keyboard-safe-input-js' not in HTML
    assert 'ar-global-input-bar' not in HTML
    assert 'function beginEdit(el,opts={})' in HTML
    assert 'vsflat-active-input' in HTML


def test_old_vehicle_garage_page_removed_but_compatibility_redirects_home_panel():
    assert SOUP.find(id='allroads-v52-vehicle-script') is None
    compat=SOUP.find(id='jepalys-v529201-compat-two-view')
    assert compat is not None
    assert 'JEPALYSFlat?.vehicleMenu' in compat.get_text()


def test_driving_has_single_navigation_to_home():
    assert "#ar-mobile-nav[data-state=\"driving\"] #ar51-back{display:none!important}" in HTML
    assert "#ar-mobile-nav[data-state=\"driving\"] #ar51-home{display:grid!important" in HTML


def test_frontend_copies_are_identical():
    assert (ROOT/'frontend/index.html').read_bytes()==(ROOT/'api/frontend/index.html').read_bytes()


def test_launcher_uses_current_package_and_stable_engine_version():
    assert 'V52.9.235' in LAUNCHER
    assert 'v=52.9.235' in LAUNCHER
    assert "V52.9.102" in LAUNCHER
