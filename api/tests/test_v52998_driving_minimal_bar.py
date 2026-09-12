from pathlib import Path
ROOT=Path(__file__).parents[2]
HTML=(ROOT/"api/frontend/index.html").read_text(encoding="utf-8")

def test_v52998_minimal_bar_rules_present():
    assert 'allroads-v52998-driving-minimal-bar' in HTML
    assert 'IDLE_MS=4200' in HTML
    assert 'STOP_CONFIRM_MS=3000' in HTML
    assert 'STOP_MAX_KMH=0.8' in HTML
    assert 'MOVE_MIN_KMH=2' in HTML
    assert 'ar52998-controls-hidden' in HTML
    assert 'ar52998-vehicle-stopped' in HTML
    assert 'ar52998-trip-engraved' in HTML
    assert 'ar52998-stop-floating' in HTML

def test_v52998_preserves_real_gps_authority():
    assert 'requestFreshPosition(12000)' in HTML
    assert 'Conduite réelle : le GPS est l\'unique autorité de position.' in HTML

def test_v52998_frontend_mirrors_identical():
    assert (ROOT/'frontend/index.html').read_bytes()==(ROOT/'api/frontend/index.html').read_bytes()
