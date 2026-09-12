from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
HTML2=(ROOT/'frontend/index.html').read_text(encoding='utf-8')
BAT=(ROOT/'AA_LANCER_JEPALYS.bat').read_text(encoding='utf-8')
SW=(ROOT/'api/frontend/sw.js').read_text(encoding='utf-8')

def test_car_reference_dimensions_and_version():
    needle="voiture: {name:'Ma voiture', height:1.50, width:1.80, length:4.40"
    assert needle in HTML
    assert needle in HTML2
    assert 'J235 · Virage Serré · Simulation propre · saisie JEPALYS' in HTML
    assert 'V52.9.235' in BAT
    assert 'v=52.9.235&launch=test-terrain-realisable' in BAT
    assert "VERSION='52.9.235'" in SW
