from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/"api/frontend/index.html").read_text(encoding="utf-8")

def test_j241_final_authority_and_field_fixes():
    assert "jepalys-j241-field-reprise-authority" in HTML
    assert "grid-template-rows:repeat(2,92px)" in HTML
    assert "height:94px" in HTML
    assert "grid-template-columns:repeat(2,minmax(0,1fr))" in HTML
    assert "ar-j241-roundabout" in HTML
    assert "className:'ar-driving-route-halo'" in HTML

def test_j241_settings_delegation_and_french_normalizer():
    assert "data-j241-mode" in HTML
    assert "function fr(t)" in HTML
    assert "Au rond-point, prenez la ${n}e sortie" in HTML

def test_j241_render_command_stays_safe():
    y=(ROOT/"render.yaml").read_text(encoding="utf-8")
    assert "buildCommand: pip install -r api/requirements.txt" in y
