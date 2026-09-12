from pathlib import Path

HTML = (Path(__file__).parents[1] / 'frontend' / 'index.html').read_text(encoding='utf-8')


def test_single_panel_authority_no_historical_wrapper():
    assert HTML.count('function panel(state)') == 1
    assert 'oldPanel=panel' not in HTML
    assert 'panel=function(state)' not in HTML


def test_prepare_has_no_stale_delayed_europe_reframe():
    assert 'ar52992PrepareNational' not in HTML
    assert 'ar52992ResolveNationalView' not in HTML
    assert 'ar52992FitNational' not in HTML
    assert "const arE7EuropeView={center:[52.0,11.5],zoom:4};" in HTML


def test_state_controller_cancels_stale_work():
    assert 'let arE7StateEpoch=0' in HTML
    assert 'function arE7CancelDeferred()' in HTML
    assert "if(epoch!==arE7StateEpoch || (root.dataset.state||'')!==expectedState)return" in HTML
    assert "arE7AfterPaint(state,()=>arE7RefreshState(state))" in HTML


def test_visual_brick_is_not_second_leaflet_controller():
    block = HTML.split('<script id="allroads-e7-visual-brick-js">',1)[1].split('</script>',1)[0]
    assert 'setMapView(' not in block
    assert 'map.invalidateSize()' not in block
    assert 'activeMapView' not in block


def test_open_restores_historical_prepare_order_then_refreshes_visible_map():
    block = HTML.split('function open(p){',1)[1].split('function close(){',1)[0]
    assert block.index("panel('prepare')") < block.index("document.body.classList.add('ar-mobile-nav-open')")
    assert "arE7AfterPaint('prepare',()=>arE7RefreshState('prepare'));" in block
