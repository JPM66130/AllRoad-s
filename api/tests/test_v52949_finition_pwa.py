from pathlib import Path
ROOT=Path(__file__).parents[2]
HTML=(ROOT/'api'/'frontend'/'index.html').read_text(encoding='utf-8')
def test_v52949_version_and_launcher():
 assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'
 launchers=list(ROOT.glob('*LANCER_ALLROADS*.bat')); assert len(launchers)==1
 assert launchers[0].name=='AA_LANCER_JEPALYS.bat'
def test_v52949_ready_safe_bottom_margin():
 assert 'height:130px!important;max-height:130px!important;bottom:11px!important' in HTML
 assert 'padding:4px 9px 11px!important' in HTML
 assert 'grid-template-rows:22px 41px 42px!important' in HTML
 assert 'height:42px!important;min-height:42px!important' in HTML
def test_v52949_driving_compact_preserved():
 assert 'data-state="driving"] .ar51-sheet{height:112px!important' in HTML
 assert 'data-state="driving"] .ar51-sheet{height:56px!important' in HTML
