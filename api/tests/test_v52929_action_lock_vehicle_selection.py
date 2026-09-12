from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "frontend" / "index.html"

def html():
    return HTML.read_text(encoding="utf-8")

def test_v52929_version_and_action_lock_present():
    s = html()
    assert "V52.9.102" in s
    assert "function ar52929SetActionLock(locked)" in s
    assert "ar52929-action-lock" in s
    assert "data-ar52929-prev-disabled" in s

def test_v52929_important_confirmations_lock_actions():
    s = html()
    assert "4000,{lockActions:true}" in s
    assert "5000,{lockActions:true}" in s
    assert "#ar52924-reached" in s
    assert "#ar51-find-turnaround" in s
    assert "#ar52919-report-blockage" in s

def test_v52929_vehicle_selection_is_unambiguous():
    s = html()
    assert "SÉLECTIONNÉ" in s
    assert "ar52-selected-check" in s
    assert "aria-current" in s
    assert "border-color:#20a99b" in s
    assert "rgba(20,145,112,.16)" in s

def test_v52929_map_controls_not_business_locked():
    s = html()
    assert "#ar51-zoom-in" in s
    assert "#ar51-zoom-out" in s
    assert "pointer-events:auto!important" in s

def test_no_unsafe_backtrack_instruction_reintroduced():
    s = html().lower()
    assert "revenez sur vos pas" not in s
