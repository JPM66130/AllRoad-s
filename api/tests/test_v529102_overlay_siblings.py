from pathlib import Path

ROOT=Path(__file__).parents[2]
HTML=(ROOT/"api/frontend/index.html").read_text(encoding="utf-8")

def test_floating_trip_overlay_is_sibling_of_mobile_nav_and_selector_targets_sibling():
    assert '<div id="ar52998-trip-engraved"' in HTML
    assert '#ar-mobile-nav[data-state="driving"].ar52998-controls-hidden ~ #ar52998-trip-engraved{' in HTML

def test_floating_bus_stop_is_sibling_and_selector_targets_sibling():
    assert '<button id="ar52998-stop-floating"' in HTML
    assert 'body.ar-profile-bus #ar-mobile-nav[data-state="driving"].ar52998-controls-hidden ~ #ar52998-stop-floating{' in HTML
