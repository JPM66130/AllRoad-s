from pathlib import Path


def test_landscape_turnaround_panel_keeps_safety_actions_visible():
    html = (Path(__file__).parents[1] / "frontend" / "index.html").read_text(encoding="utf-8")
    assert 'id="allroads-v52925-landscape-safety-panel"' in html
    assert '#ar-mobile-nav[data-state="turnaround"] .ar51-sheet' in html
    assert 'max-height:none!important' in html
    assert 'overflow:visible!important' in html
    assert '#ar-mobile-nav[data-state="turnaround"] #ar52924-reached-wrap:not([hidden])' in html
    assert 'display:grid!important' in html
    assert 'Zone atteinte · recalculer le trajet' in html
