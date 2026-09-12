from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
def test_version_and_launcher():
 assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'
 launchers=list(ROOT.glob('*LANCER_ALLROADS_V52_9_*.bat'))
 assert len(launchers)==1 and launchers[0].name=='AA_LANCER_JEPALYS.bat'
def test_shell_order_and_brand_slot():
 vehicle=HTML.index('id="ar52-back"'); brand=HTML.index('ar52-brand ar-brand-slot',vehicle); home=HTML.index('id="ar52-home"',brand); context=HTML.index('ar-standard-context',home)
 assert vehicle < brand < home < context
 assert 'data-brand-mode="standard"' in HTML and 'ar-brand-client' in HTML
def test_mobile_shell_order():
 start=HTML.index('<header class="ar51-topbar">'); end=HTML.index('</header>',start); h=HTML[start:end]
 assert h.index('id="ar51-back"') < h.index('ar51-brand ar-brand-slot') < h.index('id="ar51-home"') < h.index('ar51-profile-chip')
def test_client_branding_does_not_move_controls():
 assert 'grid-template-columns:auto minmax(82px,1fr) auto auto' in HTML
 assert '.ar-brand-slot[data-brand-mode="client"] .ar-brand-client{display:block}' in HTML
