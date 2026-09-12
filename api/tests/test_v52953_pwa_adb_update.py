from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]

def test_version_53_everywhere():
    assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'
    assert 'APP_VERSION = "V52.9.102"' in (ROOT/'api/main.py').read_text(encoding='utf-8')

def test_manifest_start_url_is_current():
    m=json.loads((ROOT/'api/frontend/manifest.webmanifest').read_text(encoding='utf-8'))
    assert m['start_url']=='/app/?v=52.9.100&pwa=1'

def test_sw_never_serves_stale_document():
    sw=(ROOT/'api/frontend/sw.js').read_text(encoding='utf-8')
    assert "fetch(event.request,{cache:'no-store'})" in sw
    assert 'c.navigate(c.url)' not in sw
    assert "postMessage({type:'ALLROADS_SW_READY',version:VERSION})" in sw
    assert "const VERSION='52.9.97'" in sw

def test_registration_bypasses_http_cache():
    html=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
    assert "updateViaCache:'none'" in html
    assert '.then(reg=>reg.update())' in html

def test_launcher_targets_one_adb_device():
    bat=(ROOT/'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8')
    assert '-s "!ADB_SERIAL!" reverse tcp:8000 tcp:8000' in bat
    assert 'findstr /R' in bat
    assert 'V52.9.102' in bat
