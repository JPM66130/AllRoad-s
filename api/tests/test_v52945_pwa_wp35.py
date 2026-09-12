from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend/index.html').read_text(encoding='utf-8')

def test_version_launcher_v52945():
    assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'
    launchers=list(ROOT.glob('*LANCER_ALLROADS_V52_9_*.bat'))
    assert len(launchers)==1 and launchers[0].name=='AA_LANCER_JEPALYS.bat'

def test_pwa_manifest_display_orientation_libre():
    m=json.loads((ROOT/'api/frontend/manifest.webmanifest').read_text(encoding='utf-8'))
    # V59 revient au plein écran prioritaire ; la coque interne est désormais figée.
    assert m['display']=='fullscreen'
    assert m.get('display_override')==['fullscreen','standalone']
    assert m['orientation']=='any'
    assert m['start_url'].startswith('/app/')
    assert len(m['icons'])>=2

def test_pwa_service_worker_and_install_ui():
    sw=(ROOT/'api/frontend/sw.js').read_text(encoding='utf-8')
    assert "addEventListener('fetch'" in sw
    assert 'rel="manifest"' in HTML
    assert 'INSTALLER ALLROAD’S' in HTML
    assert "serviceWorker.register('/app/sw.js?v=52.9.100'" in HTML

def test_launcher_adb_reverse_localhost():
    s=(ROOT/'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8')
    assert 'reverse tcp:8000 tcp:8000' in s
    assert 'http://localhost:8000/app/?v=52.9.100' in s

def test_frontend_copies_identical():
    assert (ROOT/'frontend/index.html').read_bytes()==(ROOT/'api/frontend/index.html').read_bytes()
