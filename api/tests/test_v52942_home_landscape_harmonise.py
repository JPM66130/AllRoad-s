from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend/index.html').read_text(encoding='utf-8')

def test_version_42():
    assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'
    assert 'V52.9.102' in HTML

def test_home_landscape_harmonised_without_touching_reference_views():
    assert 'allroads-v52942-home-landscape-harmonise' in HTML
    assert 'max-width:800px!important' in HTML
    assert 'object-fit:cover!important' in HTML
    assert '#allroads-mobile-home .ar-home-actions' in HTML

def test_frontend_copies_identical():
    assert (ROOT/'frontend/index.html').read_bytes()==(ROOT/'api/frontend/index.html').read_bytes()
