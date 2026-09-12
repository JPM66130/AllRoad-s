from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')

def test_version_52947():
    assert 'V52.9.102' in (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8')

def test_stability_patch_present():
    assert 'allroads-v52947-pwa-stability' in HTML
    assert 'AllRoadsDismissKeyboard' in HTML
    assert "visualViewport n'a volontairement AUCUN droit de redimensionner la coque" in HTML

def test_frontend_copies_identical():
    assert (ROOT/'api/frontend/index.html').read_bytes()==(ROOT/'frontend/index.html').read_bytes()
