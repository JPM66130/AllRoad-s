from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTMLS=[ROOT/'api/frontend/index.html',ROOT/'frontend/index.html']
LAUNCHER=ROOT/'AA_LANCER_JEPALYS.bat'

def text(p): return p.read_text(encoding='utf-8',errors='ignore')

def test_v221_identity_and_launcher():
    assert 'J235 · Virage Serré · Simulation propre · saisie JEPALYS' in text(HTMLS[0])
    assert 'V52.9.235' in text(LAUNCHER)
    assert 'v=52.9.235&launch=test-terrain-realisable' in text(LAUNCHER)

def test_j220_gray_mask_and_fake_1m_bound_are_removed():
    for p in HTMLS:
        s=text(p)
        assert '#ar220-orientation-mask' not in s
        assert 'ar220-orientation-masking' not in s
        assert 'cameraHeightM=1,behindM=1' not in s
        assert 'ar221-perspective-map' not in s
        assert 'harmonizedFarZoom' in s
        assert 'harmonizedFarZoom' in s
