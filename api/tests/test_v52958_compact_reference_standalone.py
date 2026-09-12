from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend'/'index.html').read_text(encoding='utf-8')

def test_v58_version_launcher_and_frontends():
    assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'
    assert (ROOT/'AA_LANCER_JEPALYS.bat').exists()
    assert (ROOT/'frontend'/'index.html').read_bytes()==(ROOT/'api'/'frontend'/'index.html').read_bytes()

def test_vehicle_reference_compact_present():
    assert 'allroads-v52958-vehicle-compact-reference' in HTML
    assert 'font-size:22px!important' in HTML
    assert 'height:58px!important;min-height:58px!important' in HTML
    assert 'background:#1675df!important' in HTML
    assert ".ar52-editor:not(.editing) .ar52-grid label:nth-child(6)" in HTML
    assert ".ar52-editor:not(.editing) .ar52-grid label:nth-child(7)" in HTML

def test_mapviews_stay_between_header_and_guidance():
    block=HTML.split('allroads-v52958-vehicle-compact-reference',1)[1]
    assert '#ar-mobile-nav .ar525-mapviews' in block
    assert '#ar-mobile-nav[data-state="driving"] .ar51-maneuver' in block
    assert 'z-index:210!important' in block
    assert 'z-index:205!important' in block

def test_manifest_prefers_fullscreen_with_fixed_shell():
    data=json.loads((ROOT/'frontend'/'manifest.webmanifest').read_text(encoding='utf-8'))
    assert data['display']=='fullscreen'
    assert data['display_override']==['fullscreen','standalone']
    assert data['start_url'].startswith('/app/?v=52.9.100')
