from pathlib import Path

HTML = Path(__file__).parents[1] / "frontend" / "index.html"


def test_dynamic_horizon_is_speed_based_and_bounded():
    text = HTML.read_text(encoding="utf-8")
    assert "const horizonSeconds=180" in text
    assert "Math.min(6500,Math.max(1200,speedHorizonMeters))" in text
    assert "const horizonMeters=Math.max(1,Math.min(totalAhead,desiredHorizonMeters))" in text


def test_old_remaining_route_fraction_no_longer_controls_horizon():
    text = HTML.read_text(encoding="utf-8")
    assert "Math.max(2500,totalAhead*0.65)" not in text


def test_route_visual_reference_stays_blue_without_gray_casing():
    text = HTML.read_text(encoding="utf-8")
    assert "#006CFF" in text
