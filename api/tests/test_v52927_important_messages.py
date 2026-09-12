from pathlib import Path

def test_v52927_important_messages_are_unambiguous():
    html=(Path(__file__).parents[1]/"frontend"/"index.html").read_text(encoding="utf-8")
    assert "V52.9.102" in html
    assert "ar52927-orange-confirm" in html
    assert "rgba(255,145,0,.94)" in html
    assert "color:#101010" in html
    assert "✓ TRAJET RECALCULÉ\\nBlocage exclu — vous pouvez poursuivre le guidage" in html
    assert ",5000)" in html
    assert "ar52927-recalc-confirm" in html
    assert "top:50%" in html
    assert "font-size:22px" in html
