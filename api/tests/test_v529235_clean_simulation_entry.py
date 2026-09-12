from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend'/'index.html').read_text(encoding='utf-8')

def test_demo_button_uses_same_jepalys_keyboard_path():
    assert "routeLaunchMode='simulation'" in HTML
    assert "beginEdit(to,{clear:!dest,preserve:!!dest})" in HTML
    assert "await compareDestinationInKeyboard()" in HTML

def test_simulation_diverges_only_after_real_route_is_ready():
    assert 'startSimulationDirect' in HTML
    assert "window.__allroadsRouteSimulationMode=true" in HTML
    assert "arJ232StartRouteSimulation()" in HTML
    assert "moteur synthétique historique conservé pour archive/compatibilité, non appelé par Démo sans GPS Virage Serré" in HTML
