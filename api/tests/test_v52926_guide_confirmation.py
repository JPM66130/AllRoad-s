from pathlib import Path


def test_v52926_guide_confirmation_is_visible_and_long_enough():
    html = (Path(__file__).parents[1] / "frontend" / "index.html").read_text(encoding="utf-8")
    assert "V52.9.102" in html
    assert "✓ Guidage vers la zone de retournement activé · continuez en marche avant" in html
    assert "4000,{lockActions:true}" in html
    assert "ar52926-guide-confirm" in html
    assert "bottom:190px!important" in html
    assert "bottom:370px!important" in html
