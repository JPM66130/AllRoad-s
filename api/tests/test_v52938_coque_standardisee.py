from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend/index.html').read_text(encoding='utf-8')

def test_version_and_launcher():
    assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'
    launchers=list(ROOT.glob('*LANCER_ALLROADS_V52_9_*.bat'))
    assert len(launchers)==1 and launchers[0].name=='AA_LANCER_JEPALYS.bat'

def test_standard_shell_navigation_order():
    assert 'ar52-head ar-standard-head' in HTML
    h=HTML.split('<header class="ar52-head ar-standard-head">',1)[1].split('</header>',1)[0]
    assert h.index('id="ar52-back"') < h.index('ar52-brand ar-brand-slot') < h.index('id="ar52-home"') < h.index('ar-standard-context')
    assert 'Menu principal' not in HTML

def test_driving_bar_final_balance():
    assert 'grid-template-columns:50px repeat(4,minmax(0,1fr)) 50px' in HTML
    assert 'border:1px solid #b8d9ea' in HTML
    assert 'font-size:10.5px' in HTML

def test_frontend_copies_identical():
    assert (ROOT/'frontend/index.html').read_bytes()==(ROOT/'api/frontend/index.html').read_bytes()
