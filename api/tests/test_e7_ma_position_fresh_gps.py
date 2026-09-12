from pathlib import Path

HTML = (Path(__file__).parents[1] / 'frontend' / 'index.html').read_text(encoding='utf-8')

def test_ma_position_ne_reutilise_jamais_le_marqueur_leaflet():
    block = HTML[HTML.index('async function arE7ResolveRoutePoint'):HTML.index('async function previewExisting')]
    assert "AllRoadsGpsRuntime.requestFreshPosition" in block
    assert "getCurrentPosition" not in block
    assert "vehicleMarker" not in block
    assert "source:'gps'" in block

def test_destination_recoit_le_depart_gps_comme_focus():
    block = HTML[HTML.index('async function previewExisting'):HTML.index('// V52.8.1')]
    assert 'arE7ResolveRoutePoint(dest,1,startPlace)' in block
