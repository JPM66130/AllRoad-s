from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
API = ROOT / "api" / "frontend" / "index.html"
MIRROR = ROOT / "frontend" / "index.html"

def test_j240_keyboard_predictive_and_mirrored():
    a = API.read_text(encoding="utf-8")
    b = MIRROR.read_text(encoding="utf-8")
    assert a == b
    assert 'id="vs240-kb-suggestions"' in a
    assert "function scheduleKeyboardSuggestions()" in a
    assert "jepalys-kb-learned-v240" in a
    assert "fetch('/poi/search?'" in a
    assert "setTimeout(async()=>" in a and ",320)" in a
    assert "kbChoosePlace" in a
    assert "delete activeEdit.dataset.poiLat" in a

def test_j240_service_worker_cache_busted_for_final_package():
    sw1 = (ROOT / "api" / "frontend" / "sw.js").read_text(encoding="utf-8")
    sw2 = (ROOT / "frontend" / "sw.js").read_text(encoding="utf-8")
    assert sw1 == sw2
    assert "jepalys-v52-9-240-final" in sw1
    assert "sw.js?v=52.9.240-final" in API.read_text(encoding="utf-8")
