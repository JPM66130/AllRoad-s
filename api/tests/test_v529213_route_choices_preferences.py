from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HTML = (ROOT / 'api/frontend/index.html').read_text(encoding='utf-8')
ROUTER = (ROOT / 'api/routers/itineraires.py').read_text(encoding='utf-8')
GEO = (ROOT / 'api/utils/geo.py').read_text(encoding='utf-8')
LAUNCHER = (ROOT / 'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8', errors='ignore')


def test_j213_visible_and_launcher_fresh():
    assert 'J235 · Virage Serré · Simulation propre · saisie JEPALYS' in HTML
    assert 'V52.9.235' in LAUNCHER
    assert 'v=52.9.235&launch=test-terrain-realisable' in LAUNCHER


def test_test_profiles_are_grey_but_dev_clickability_is_preserved():
    assert 'vs213-test-internal' in HTML
    assert "!['voiture','bus'].includes(p)" in HTML
    assert 'TEST INTERNE' in HTML
    assert 'ALLROADS_DEV_ALL_PROFILES = true' in HTML


def test_three_route_comparison_and_persistent_preferences_exist():
    assert '@router.get("/comparaison")' in ROUTER
    assert '("Recommandé", "recommended")' in ROUTER
    assert '("Le plus rapide", "fastest")' in ROUTER
    assert '("Le plus court", "shortest")' in ROUTER
    assert 'avoid_autoroutes' in HTML and 'avoid_peages' in HTML and 'avoid_ferries' in HTML
    assert 'jepalys-route-preferences-v213' in HTML


def test_route_preferences_reach_ors_and_motorway_is_not_toll():
    assert 'options["avoid_features"] = avoid_features' in GEO
    assert '"highways"' in ROUTER and '"tollways"' in ROUTER and '"ferries"' in ROUTER
    assert 'peages_eur = 0.0 if avoid_peages else None' in ROUTER
    assert 'autoroute ne signifie pas péage' in ROUTER


def test_cost_uses_active_vehicle_consumption():
    assert 'consommation_l_100' in ROUTER
    assert 'fuel_l = round(route["distance_km"] * consommation / 100, 1)' in ROUTER
    assert 'consommation_l' in HTML and 'cout_total_eur' in HTML
