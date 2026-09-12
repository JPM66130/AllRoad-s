from pathlib import Path

ROOT = Path(__file__).parents[2]
HTML = (ROOT / "api" / "frontend" / "index.html").read_text(encoding="utf-8")
LAUNCHER = (ROOT / "AA_LANCER_JEPALYS.bat").read_text(encoding="utf-8")

def test_one_panel_authority_only():
    assert HTML.count("function panel(state)") == 1

def test_one_gps_watch_only():
    assert HTML.count("navigator.geolocation.watchPosition(") == 1

def test_launcher_forces_fresh_test_navigation():
    assert "v=52.9.199" in LAUNCHER
