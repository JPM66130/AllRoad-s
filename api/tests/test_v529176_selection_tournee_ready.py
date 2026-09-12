from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HTML = (ROOT / 'api' / 'frontend' / 'index.html').read_text(encoding='utf-8')
MIRROR = (ROOT / 'frontend' / 'index.html').read_text(encoding='utf-8')

def test_v176_frontends_match():
    assert HTML == MIRROR

def test_v176_vehicle_selection_is_reinforced():
    assert 'jepalys-v529176-selection-tournee-ready' in HTML
    assert ".ar-home-selected-title::after{content:'  ✓ ACTIF'" in HTML
    assert 'ar176-vehicle-chip' in HTML

def test_v176_bus_tournee_is_explicit_and_saved_only():
    assert 'id="ar176-tournee-prepare"' in HTML
    assert 'id="ar176-tournee-ready"' in HTML
    assert "filter(x=>x.sauvegarde_volontaire)" in HTML
    assert "apiFetch('/itineraire/')" in HTML
    assert "from.value=item.depart" in HTML
    assert "to.value=item.arrivee" in HTML

def test_v176_does_not_auto_recalculate_selected_tournee():
    segment = HTML.split('async function ar176OpenTournees()',1)[1].split("window.addEventListener('pagehide'",1)[0]
    assert 'previewExisting()' not in segment
    assert 'startDriving()' not in segment

def test_v176_ready_landscape_single_compact_bar():
    assert 'grid-template-columns:180px minmax(220px,1fr) 190px!important' in HTML
    assert '.ar51-ready-inline .ar51-actions{grid-column:3!important;grid-row:1!important;position:static!important' in HTML
