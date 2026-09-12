from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_stopped_bar_timeout_and_no_forced_visibility():
    html=(ROOT/"api/frontend/index.html").read_text(encoding="utf-8")
    assert "STOP_IDLE_MS=20000" in html
    assert "stopped?STOP_IDLE_MS:IDLE_MS" in html
    assert "function hide(){if(!isDriving())return;" in html
    assert 'ar52998-vehicle-stopped .ar51-sheet{transform:none!important' not in html
    assert "ar52998-stop-floating" in html
