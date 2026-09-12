from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/"api/frontend/index.html").read_text(encoding="utf-8")
SW=(ROOT/"api/frontend/sw.js").read_text(encoding="utf-8")
LAUNCHER=(ROOT/"AA_LANCER_JEPALYS.bat").read_text(encoding="utf-8")

def test_j211_mobile_hud_uses_calculated_route():
    assert "J211 — la coque mobile ne garde plus les valeurs de démonstration" in HTML
    assert "mobileLeft.textContent = distanceKm" in HTML
    assert "mobileTime.textContent = formatDuration(totalMinutes)" in HTML
    assert "totalMinutes * 60000" in HTML

def test_j211_mobile_hud_tracks_gps_remaining_route():
    assert "J211 — distance/temps/heure d’arrivée de la coque mobile suivent le trajet réel" in HTML
    assert "remainingKm = Math.max(0, progress.totalKm - progress.travelledKm)" in HTML
    assert "routeTotalMinutes * remainingKm / progress.totalKm" in HTML

def test_j211_keyboard_brand_and_transparency():
    assert 'id="vs207-kb-logo"' in HTML
    assert "background:rgba(2,24,38,.68)" in HTML

def test_j211_cache_and_launcher_fresh():
    assert "52.9.235" in SW
    assert "V52.9.235" in LAUNCHER
    assert "v=52.9.235&launch=test-terrain-realisable" in LAUNCHER
    assert "J235 · Virage Serré · Simulation propre · saisie JEPALYS" in HTML
