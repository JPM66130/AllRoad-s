from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / 'frontend' / 'index.html'
API_INDEX = ROOT / 'api' / 'frontend' / 'index.html'


def html():
    return INDEX.read_text(encoding='utf-8')


def test_v52952_version_and_frontend_copies():
    text = html()
    assert 'V52.9.102' in text
    assert INDEX.read_bytes() == API_INDEX.read_bytes()


def test_ready_action_continuity_modifier_then_start():
    text = html()
    marker = '<div class="ar51-actions"><button class="ar51-secondary" id="ar51-edit" type="button">Modifier</button><button class="ar51-primary" id="ar51-start" type="button">Démarrer</button></div>'
    assert marker in text
    assert '#ar-mobile-nav[data-state="ready"] #ar51-edit{grid-column:1!important}' in text
    assert '#ar-mobile-nav[data-state="ready"] #ar51-start{grid-column:2!important}' in text


def test_vehicle_confirmation_finishes_portrait_view():
    text = html()
    assert 'body.ar52-vehicle-open .ar52-confirm{' in text
    assert 'margin-top:auto!important' in text
    assert 'padding-bottom:var(--ar-panel-bottom-gap,6px)!important' in text


def test_installed_pwa_freezes_resize_between_rotations():
    text = html()
    assert "const standalone=window.matchMedia('(display-mode: standalone)').matches" in text
    assert "if(!standalone){\n    window.addEventListener('resize'" in text
    assert "document.documentElement.classList.toggle('ar-standalone-stable',standalone);" in text
    assert 'visualViewport reste réservé au clavier' in text


def test_sw_cache_bumped():
    sw = (ROOT / 'frontend' / 'sw.js').read_text(encoding='utf-8')
    assert 'allroads-v52-9-95' in sw
    assert 'allroads-v52-9-51-shell' not in sw
