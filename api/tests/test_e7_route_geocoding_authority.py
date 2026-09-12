from pathlib import Path
HTML=(Path(__file__).parents[1]/'frontend'/'index.html').read_text(encoding='utf-8')
def test_mobile_route_geocodes_both_visible_endpoints_before_submit():
    a=HTML.index('async function previewExisting()'); block=HTML[a:HTML.index('// V52.8.1',a)]
    assert 'arE7ResolveRoutePoint(from,0)' in block
    assert 'arE7ResolveRoutePoint(dest,1,startPlace)' in block
    assert "document.getElementById('lat1').value=startPlace.latitude" in block
    assert "document.getElementById('lat2').value=endPlace.latitude" in block
    assert block.index('arE7ResolveRoutePoint(from,0)') < block.index('requestSubmit()')
def test_ma_position_uses_real_position_not_demo_coordinates():
    a=HTML.index('async function arE7ResolveRoutePoint'); block=HTML[a:HTML.index('async function previewExisting()',a)]
    assert 'AllRoadsGpsRuntime.requestFreshPosition' in block
    assert 'getCurrentPosition' not in block
    assert '42.6711' not in block and '42.6456' not in block
