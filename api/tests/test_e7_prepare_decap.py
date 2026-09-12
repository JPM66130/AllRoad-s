from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
CSS=(ROOT/'api/frontend/allroads_ui_final.css').read_text(encoding='utf-8')

def test_prepare_css_is_single_clean_authority():
    assert CSS.count('E7 CLEAN — PREPARER / READY : autorité cartographique unique') == 1
    assert 'opacity:.16!important' not in CSS
    assert 'opacity:.08!important' not in CSS
    assert 'body.ar5285-view-prepare #map::before' in CSS
    assert 'content:none!important' in CSS

def test_prepare_no_map_green_paint_late_rule():
    assert 'body.ar5285-view-prepare #ar-mobile-nav,body.ar5285-view-prepare #map{background-color:#dfe8e3!important}' not in CSS

def test_prepare_uses_fresh_css_token_and_historical_open_order():
    assert '/app/allroads_ui_final.css?v=52.9.91' in HTML
    block=HTML[HTML.index('  function open(p){', HTML.index('// E7 — contrôleur')):]
    assert block.index("panel('prepare');") < block.index("document.body.classList.add('ar-mobile-nav-open');")
    assert "arE7AfterPaint('prepare',()=>arE7RefreshState('prepare'));" in block
