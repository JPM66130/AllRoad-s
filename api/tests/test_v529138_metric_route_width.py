from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEXES = [ROOT/'api/frontend/index.html', ROOT/'frontend/index.html']


def test_metric_route_width_formula_and_margin_present():
    for p in INDEXES:
        text = p.read_text(encoding='utf-8')
        assert 'function arRouteVehicleWidthMeters()' in text
        assert 'function arRouteMetricWeightPx' in text
        assert 'arRouteVehicleWidthMeters()*1.05' in text
        assert '156543.03392804097*Math.cos(latitude)' in text
        assert "bus:2.55,poids_lourd:2.55" in text
        assert "Number(document.getElementById('largeur_m')?.value)" in text


def test_metric_width_applied_to_ready_and_driving_route():
    for p in INDEXES:
        text = p.read_text(encoding='utf-8')
        assert 'arApplyMetricRouteWidth();' in text
        assert "const weight=arRouteMetricWeightPx();" in text
        assert "className:'ar-driving-route-core'" in text
        assert "map.on('zoomend moveend',()=>{try{arApplyMetricRouteWidth();arBringDrivingRouteToFront()}catch(_){}});" in text
        assert "arRouteVisualCoverScale=scale;" in text
