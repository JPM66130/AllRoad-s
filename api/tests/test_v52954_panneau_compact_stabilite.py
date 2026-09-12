from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend'/'index.html').read_text(encoding='utf-8')
SW=(ROOT/'frontend'/'sw.js').read_text(encoding='utf-8')

def test_v52954_version_launcher_and_copies():
    assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'
    assert (ROOT/'AA_LANCER_JEPALYS.bat').exists()
    assert (ROOT/'frontend'/'index.html').read_bytes()==(ROOT/'api'/'frontend'/'index.html').read_bytes()

def test_prepare_fronton_compact_portrait():
    assert 'allroads-v52954-prepare-fronton-compact' in HTML
    assert 'position:absolute!important;top:5px!important' in HTML
    assert 'padding-top:10px!important' in HTML

def test_test_bridge_does_not_poll_in_driver_mode():
    assert "get('testbridge')==='1'" in HTML
    assert 'if(testBridgeEnabled)' in HTML

def test_service_worker_never_forces_open_window_navigation():
    assert 'c.navigate(c.url)' not in SW
    assert "ALLROADS_SW_READY" in SW
    assert "cache:'no-store'" in SW
