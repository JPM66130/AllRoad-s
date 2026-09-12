from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HTML = (ROOT / "api/frontend/index.html").read_text(encoding="utf-8")
LAUNCHER = (ROOT / "AA_LANCER_JEPALYS.bat").read_text(encoding="utf-8", errors="replace")

def test_tour_load_goes_directly_to_calculation_and_driving():
    assert "async function launchTourDirect(t)" in HTML
    assert "calculateHeadless?.(pkey(),e.from,e.to" in HTML
    assert "p.querySelectorAll('[data-load]').forEach(b=>b.onclick=()=>launchTourDirect" in HTML
    assert "p.querySelectorAll('[data-return]').forEach(b=>b.onclick=()=>launchTourDirect(reverseTour" in HTML
    assert "autoStart=true" in HTML

def test_tour_direct_does_not_open_destination_keyboard():
    segment = HTML.split("async function launchTourDirect(t)",1)[1].split("function tourMenu()",1)[0]
    assert "beginEdit(" not in segment
    assert "compareDestinationInKeyboard(" not in segment
    assert "ensureKeyboard(" not in segment

def test_j216_identity():
    assert "J235 · Virage Serré · Simulation propre · saisie JEPALYS" in HTML
    assert "V52.9.235" in LAUNCHER
    assert "v=52.9.235&launch=test-terrain-realisable" in LAUNCHER
