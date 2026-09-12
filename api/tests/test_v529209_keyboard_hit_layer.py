from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/"api/frontend/index.html").read_text(encoding="utf-8")
SW=(ROOT/"api/frontend/sw.js").read_text(encoding="utf-8")

def test_j210_removes_failed_hit_layer():
    assert "vs209-input-hit" not in HTML
    assert "vs209-edit-host" not in HTML

def test_j210_keyboard_is_child_of_visible_home():
    assert "const host=by('allroads-mobile-home')||document.body;host.appendChild(k)" in HTML
    assert "document.body.appendChild(k)" not in HTML

def test_j210_keyboard_sits_above_home_stack():
    assert "z-index:2147483600" in HTML
    assert "#allroads-mobile-home.ar-home" in HTML
    assert "z-index:99999" in HTML

def test_j210_single_home_delegation():
    assert "root.dataset.vs210KeyboardDelegation" in HTML
    assert "home.addEventListener('click'" in HTML
    assert "document.addEventListener('pointerdown',open,true)" not in HTML
    assert "editableFromTarget" in HTML

def test_j210_fresh_cache_and_visible_version():
    assert "J235 · Virage Serré · Simulation propre · saisie JEPALYS" in HTML
    assert "/app/sw.js?v=52.9.235" in HTML
    assert "jepalys-v52-9-220" in SW
