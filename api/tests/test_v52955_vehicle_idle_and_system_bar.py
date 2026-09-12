from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/"frontend/index.html").read_text(encoding="utf-8")

def test_v55_identity():
    assert (ROOT/"VERSION_DEMO.txt").read_text(encoding="utf-8").strip()=="V52.9.102"
    assert (ROOT/"AA_LANCER_JEPALYS.bat").exists()

def test_vehicle_characteristics_are_permanent_and_locked_at_rest():
    assert "Caractéristiques du véhicule" in HTML
    assert ".ar52-editor{display:block" in HTML
    assert ".ar52-editor:not(.editing) input" in HTML
    assert "i.readOnly=!open" in HTML
    assert "idleEditor()" in HTML

def test_system_bar_stability_uses_large_viewport():
    assert "viewport-fit=cover" in HTML
    assert "interactive-widget=overlays-content" in HTML
    assert "allroads-v52955-system-bars-stable" in HTML
    assert "height:100lvh!important" in HTML

def test_frontends_match():
    assert (ROOT/"frontend/index.html").read_bytes()==(ROOT/"api/frontend/index.html").read_bytes()
