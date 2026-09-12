from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / 'frontend' / 'index.html'

def text():
    return HTML.read_text(encoding='utf-8')

def test_route_simulation_keeps_real_map_visual_mode():
    s=text()
    assert "window.__allroadsRouteSimulationMode=false" in s
    assert "window.__allroadsRouteSimulationMode?'real':(window.__allroadsDemoMode?'demo':'real')" in s
    assert "window.__allroadsRouteSimulationMode=true;clearDemo();arE7ClearLegacyVisuals();" in s
    assert "if(driving && (!demoMode||window.__allroadsRouteSimulationMode))focusDrivingRoute();" in s
    assert "if(arE7DrivingStates.has(state) && (!demoMode||window.__allroadsRouteSimulationMode))" in s
    assert 'arJ232StopRouteSimulation(false);window.AllRoadsDrivingSpeed?.simulation(0);' in s

def test_frontend_mirrors_identical_j233():
    a=Path(__file__).resolve().parents[1] / 'frontend' / 'index.html'
    b=Path(__file__).resolve().parents[2] / 'frontend' / 'index.html'
    assert a.read_bytes()==b.read_bytes()
