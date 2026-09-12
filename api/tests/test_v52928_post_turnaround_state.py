from pathlib import Path

def test_v52928_post_turnaround_returns_to_normal_action_state():
    html=(Path(__file__).parents[1]/"frontend"/"index.html").read_text(encoding="utf-8")
    assert "V52.9.102" in html
    assert 'id="allroads-v52928-post-turnaround-clean-state"' in html
    assert '#ar-mobile-nav[data-state="driving"] #ar51-incident{' in html
    assert 'background:#e7f7f1!important;color:#12664f!important' in html
    assert '#ar-mobile-nav[data-state="driving"] #ar52919-report-blockage{' in html
    assert 'background:#fff0f0!important;color:#a92727!important' in html
    assert "document.getElementById('ar51-incident')?.blur();" in html
    assert "document.getElementById('ar52924-reached')?.blur();" in html
    # Les confirmations critiques validées restent intactes.
    assert "✓ TRAJET RECALCULÉ\\nBlocage exclu — vous pouvez poursuivre le guidage" in html
    assert ",5000)" in html
    # Aucune consigne dangereuse de recul ne doit réapparaître dans ce flux.
    assert "Revenez sur vos pas" not in html
