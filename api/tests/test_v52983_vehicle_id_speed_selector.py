from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend/index.html').read_text(encoding='utf-8')
CSS=(ROOT/'frontend/allroads_ui_final.css').read_text(encoding='utf-8')
JS=(ROOT/'frontend/allroads_ui_final.js').read_text(encoding='utf-8')

def test_v83_version_and_authority():
    assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'
    assert 'allroads_ui_final.css?v=52.9.91' in HTML
    assert 'allroads_ui_final.js?v=52.9.91' in HTML
    assert (ROOT/'AA_LANCER_JEPALYS.bat').exists()

def test_prepare_actions_stay_inside_landscape_frame():
    assert 'minmax(176px,.64fr)' in CSS
    assert '.ar526-prepare-actions button{' in CSS
    assert 'min-width:0!important;width:100%!important' in CSS

def test_vehicle_identification_load_and_report():
    assert 'Identification du véhicule' in JS
    assert 'allroads-vehicles-v52-' in JS
    assert 'loadVehicleByIdentifier' in JS
    assert 'identifier' in JS
    assert 'vehicle_identifier:' in HTML
    assert 'Identification : ${report.vehicle_identifier}' in HTML

def test_speed_selector_has_touch_authority_and_persistence():
    assert 'z-index:2147482985!important' in CSS
    assert "'.ar52967-speed-units [data-speed-unit]'" in JS
    assert "localStorage.getItem('allroads-speed-unit')" in JS
    assert 'setSpeedUnitFinal' in JS
