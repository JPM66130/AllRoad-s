from pathlib import Path
HTML = (Path(__file__).parents[1] / "frontend" / "index.html").read_text(encoding="utf-8")

def test_prepare_has_dedicated_europe_entry_on_main_map():
    assert "const arE7EuropeView={center:[52.0,11.5],zoom:4};" in HTML
    block=HTML.split('function arE7RefreshState(state,attempt=0){',1)[1].split('function panel(state){',1)[0]
    assert "if(state==='prepare')" in block
    assert 'map.setView(arE7EuropeView.center,arE7EuropeView.zoom,{animate:false})' in block
