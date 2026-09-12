from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/"api/frontend/index.html").read_text(encoding="utf-8")

def test_diag_rollback_and_gps_rule_preserved():
    assert "DIAG GÉOCODAGE" not in HTML
    assert "ar-e7-geo-diagnostic" not in HTML
    assert "AllRoadsGpsRuntime.requestFreshPosition(12000)" in HTML
    assert "requestFreshReliablePosition" in HTML
    assert "maxFixAgeMs:15000" in HTML or "15000" in HTML
    assert "document.getElementById('route-form')?.requestSubmit()" in HTML
