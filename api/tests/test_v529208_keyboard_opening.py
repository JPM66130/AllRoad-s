from pathlib import Path

HTML = Path("api/frontend/index.html").read_text(encoding="utf-8")
LAUNCHER = Path("AA_LANCER_JEPALYS.bat").read_text(encoding="utf-8")

def test_v208_launcher_token():
    assert "V52.9.235" in LAUNCHER
    assert "v=52.9.235" in LAUNCHER

def test_keyboard_uses_one_delegated_authority():
    assert "function installKeyboardDelegation()" in HTML
    assert "home.addEventListener('click'" in HTML
    assert "installKeyboardDelegation();installTwoViewGuard()" in HTML
    assert "el.addEventListener('pointerdown',open)" not in HTML

def test_dynamic_inputs_are_still_bound():
    assert "bindEditable(p)" in HTML
    assert "input[data-vs207-keyboard=\"1\"]" in HTML

def test_original_input_mode_is_preserved_for_numeric_keypad():
    assert "el.dataset.vs207Inputmode=el.getAttribute('inputmode')||'text'" in HTML
    assert "el?.dataset?.vs207Inputmode" in HTML
