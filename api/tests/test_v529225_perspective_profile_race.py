from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')

def test_async_perspective_race_source_removed_entirely():
    assert 'ar225PerspectiveSeq' not in HTML
    assert 'ar225PerspectiveContextValid' not in HTML
    assert 'ar221Disable' not in HTML
    assert 'ar221-perspective-drive' not in HTML

def test_car_real_dimensions_preserved():
    assert "voiture: {name:'Ma voiture', height:1.50, width:1.80, length:4.40" in HTML
