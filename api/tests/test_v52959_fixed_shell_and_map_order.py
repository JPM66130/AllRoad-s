from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend/index.html').read_text(encoding='utf-8')

def test_version_59():
    assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'
    assert 'V52.9.102' in (ROOT/'api/main.py').read_text(encoding='utf-8')

def test_pwa_fullscreen_primary_again():
    m=json.loads((ROOT/'frontend/manifest.webmanifest').read_text(encoding='utf-8'))
    assert m['display']=='fullscreen'
    assert m['display_override'][0]=='fullscreen'
    assert m['start_url']=='/app/?v=52.9.100&pwa=1'

def test_single_fixed_shell_authority_present():
    assert 'allroads-v52959-fixed-shell-js' in HTML
    assert 'allroads-v52962-single-shell-authority' in HTML
    authority=HTML.split('allroads-v52962-single-shell-authority',1)[1].split('</script>',1)[0]
    assert 'ancien verrou de coque neutralisé' in authority
    assert 'JEPALYSShell244' in HTML
    assert '100dvh' in HTML

def test_map_selector_before_guidance_geometry():
    assert 'allroads-v52959-shell-reference' in HTML
    assert '--ar59-mapviews-h:46px' in HTML
    assert '#ar-mobile-nav .ar525-mapviews' in HTML
    assert '#ar-mobile-nav[data-state="driving"] .ar51-maneuver' in HTML
    assert 'var(--ar59-mapviews-h) + var(--ar59-gap)' in HTML

def test_header_uses_viewport_edge_not_safe_area_offset():
    block=HTML.split('allroads-v52959-shell-reference',1)[1]
    assert 'top:var(--ar59-edge)!important' in block
    assert 'env(safe-area-inset-top' not in block.split('</style>',1)[0]

def test_frontend_mirror_exact():
    assert (ROOT/'frontend/index.html').read_bytes()==(ROOT/'api/frontend/index.html').read_bytes()
    assert (ROOT/'frontend/manifest.webmanifest').read_bytes()==(ROOT/'api/frontend/manifest.webmanifest').read_bytes()
    assert (ROOT/'frontend/sw.js').read_bytes()==(ROOT/'api/frontend/sw.js').read_bytes()
