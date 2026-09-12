from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend/index.html').read_text(encoding='utf-8')
SOUP=BeautifulSoup(HTML,'html.parser')

def test_v202_keeps_stable_engine_marker():
    assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'

def test_v202_home_prewarms_single_gps_authority():
    assert "try{window.AllRoadsGpsRuntime?.prepare?.()}catch(_){}" in HTML
    assert "const liveFresh = () => lastReliablePosition && isFreshReliablePreparationPosition(lastReliablePosition)" in HTML
    assert "if (watchId === null) startPreparationGpsSearch();" in HTML

def test_v202_free_route_preserves_two_view_flow():
    assert "compareHeadless?.(v.p,v.from,v.to,prefs)" in HTML
    assert "calculateHeadless?.(ctx.v.p,ctx.v.from,ctx.v.to" in HTML
    assert "window.addEventListener('allroads:route-ready'" in HTML
    assert "startDrive()" in HTML
    assert SOUP.select_one('.ar51-state-panel[data-panel="prepare"]') is None
    assert SOUP.select_one('.ar51-state-panel[data-panel="ready"]') is None

def test_v202_routing_error_returns_to_home():
    assert "phase:'routing'" in HTML
    assert "window.dispatchEvent(new CustomEvent('allroads:route-error'" in HTML

def test_v202_destination_manual_edit_restores_my_position():
    assert "if(f)f.value='Ma position'" in HTML
    assert "Départ : Ma position · saisissez la nouvelle destination." in HTML

def test_v202_input_panel_is_compact_and_high():
    assert "top:4px!important;left:10px!important;right:10px!important" in HTML
    assert "height:46px!important;min-height:46px!important" in HTML

def test_frontends_match():
    assert (ROOT/'frontend/index.html').read_bytes()==(ROOT/'api/frontend/index.html').read_bytes()
