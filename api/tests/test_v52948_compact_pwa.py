from pathlib import Path

HTML=(Path(__file__).parents[1]/"frontend"/"index.html").read_text(encoding="utf-8")

def test_v52948_compact_css_present():
    assert 'id="allroads-v52948-compact-pwa"' in HTML
    assert 'data-state="ready"' in HTML
    assert 'height:130px!important' in HTML
    assert 'height:112px!important' in HTML
    assert 'height:56px!important' in HTML

def test_v52948_ready_buttons_preserved():
    assert 'id="ar51-start"' in HTML
    assert 'id="ar51-edit"' in HTML
    assert '>Démarrer<' in HTML
    assert '>Modifier<' in HTML

def test_v52948_safety_views_not_hidden():
    assert 'data-panel="turnaround"' in HTML
    assert 'data-panel="incident"' in HTML
