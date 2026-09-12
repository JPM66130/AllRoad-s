from pathlib import Path

HTML = Path(__file__).parents[1] / "frontend" / "index.html"

def text(): return HTML.read_text(encoding="utf-8")

def test_prepare_anticipates_gps_search_without_guessing_position():
    s=text()
    assert "function startPreparationGpsSearch()" in s
    assert "if(state==='prepare') window.AllRoadsGpsRuntime?.prepare?.();" in s
    assert "maximumAge:0" in s
    assert "GPS_PREP_FRESH_MS = 15000" in s
    assert "isFreshReliablePreparationPosition" in s

def test_ma_position_waits_for_preparation_fix_and_does_not_use_marker():
    s=text()
    start=s.index("async function arE7ResolveRoutePoint")
    end=s.index("async function previewExisting", start)
    block=s[start:end]
    assert "requestFreshPosition(12000)" in block
    assert "vehicleMarker" not in block
    assert "getCurrentPosition" not in block
    assert "Recherche de votre position GPS…" in s

def test_single_native_geolocation_authority_entrypoint():
    s=text()
    assert s.count("navigator.geolocation.watchPosition(") == 1
    start=s.index("async function arE7ResolveRoutePoint")
    end=s.index("async function previewExisting", start)
    assert "navigator.geolocation.getCurrentPosition(" not in s[start:end]
