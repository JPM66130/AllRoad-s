from pathlib import Path

HTML = Path("api/frontend/index.html").read_text(encoding="utf-8")
LAUNCHER = Path("AA_LANCER_JEPALYS.bat").read_text(encoding="utf-8")

def test_v207_launcher_and_token():
    assert "V52.9.235" in LAUNCHER
    assert "v=52.9.235" in LAUNCHER

def test_custom_keyboard_is_fullscreen_and_translucent():
    assert "#vs207-keyboard" in HTML
    assert "position:fixed;inset:0" in HTML
    assert "background:rgba(2,24,38,.68)" in HTML

def test_native_android_keyboard_is_neutralized():
    assert "el.readOnly=true" in HTML
    assert "el.setAttribute('inputmode','none')" in HTML

def test_keyboard_has_explicit_validate_and_close():
    assert 'id="vs207-kb-validate"' in HTML
    assert 'id="vs207-kb-close"' in HTML
    assert "closeKeyboard(false)" in HTML
    assert "confirmActiveEdit()" in HTML

def test_j249_destination_keeps_manual_origin_and_clears_entry_buffer():
    assert "if(el.id==='vsflat-to')" in HTML
    assert "f.value='Ma position'" not in HTML
    assert "kbBuffer=''" in HTML

def test_numeric_and_azerty_layouts_exist():
    assert "keyboardMode(el)" in HTML
    assert "['A','Z','E','R','T','Y','U','I','O','P']" in HTML
    assert "if(kbMode==='decimal')" in HTML
