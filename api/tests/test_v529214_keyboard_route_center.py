from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
LAUNCHER=(ROOT/'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8',errors='ignore')

def test_route_preferences_leave_home_and_live_in_keyboard():
    assert 'id="vs213-prefs"' not in HTML
    assert 'id="vs214-kb-route-panel"' in HTML
    assert 'id="vs214-kb-prefs"' in HTML
    assert 'destination-mode' in HTML

def test_three_routes_render_inside_keyboard_and_use_vehicle_context():
    assert 'renderKeyboardRouteChoices' in HTML
    assert ".slice(0,3)" in HTML
    assert 'consommation_l' in HTML and 'cout_total_eur' in HTML
    assert 'compareDestinationInKeyboard' in HTML
    assert 'launchKeyboardRoute' in HTML

def test_landscape_keyboard_and_route_panel_are_side_by_side():
    assert '#vs207-keyboard.destination-mode #vs214-kb-route-panel{grid-column:2' in HTML
    assert 'grid-template-columns:clamp(360px,43vw,420px) minmax(0,1fr)' in HTML

def test_version_214_launcher():
    assert 'V52.9.235' in LAUNCHER
    assert 'v=52.9.235&launch=test-terrain-realisable' in LAUNCHER
