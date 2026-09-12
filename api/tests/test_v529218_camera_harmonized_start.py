from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HTMLS = [ROOT / "api/frontend/index.html", ROOT / "frontend/index.html"]


def text(path):
    return path.read_text(encoding="utf-8")


def test_launcher_219_from_harmonized_base():
    bat = text(ROOT / "AA_LANCER_JEPALYS.bat")
    assert "V52.9.235" in bat
    assert "v=52.9.235&launch=test-terrain-realisable" in bat


def test_harmonized_metric_start_zoom_present_in_both_frontends():
    for path in HTMLS:
        s = text(path)
        assert "function harmonizedFarZoom(lat)" in s
        assert "const targetMetersPerPixel=.90" in s
        assert "function metricZoomForHorizon(lat,horizon)" in s
        assert "let z=metricZoomForHorizon(anchor.lat,horizonMeters);" in s
        assert "ar221-perspective-map" not in s
        assert "AllRoadsCamera226" in s
        assert "orientationChanged" in s


def test_no_full_route_fallback_when_gps_temporarily_stale():
    for path in HTMLS:
        s = text(path)
        assert "holding-camera-no-fresh-gps" in s
        assert "arE7LastDrivingCamera" in s
        block = s[s.index("if(!rawPos||pts.length<2){"):s.index("// Nettoyage AVANT toute projection")]
        assert "map.fitBounds" not in block
