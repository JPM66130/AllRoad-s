from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / 'frontend' / 'index.html'
TEXT = HTML.read_text(encoding='utf-8')


def test_prepare_return_has_explicit_cleanup_authority():
    assert 'function arE7ResetForPrepare()' in TEXT
    assert "if(state==='ready'){saveRouteDraft();arE7ResetForPrepare();panel('prepare');return}" in TEXT


def test_edit_to_prepare_uses_same_cleanup():
    assert "ar51-edit').addEventListener('click',()=>{saveRouteDraft();arE7ResetForPrepare();panel('prepare')" in TEXT


def test_prepare_cleanup_removes_route_and_driving_residue():
    block = TEXT.split('function arE7ResetForPrepare(){',1)[1].split('\n  function panel(state){',1)[0]
    for token in [
        "clearDrivingBearing()",
        "clearDemo()",
        "map.removeLayer(routeLayer)",
        "arE7ClearLegacyVisuals()",
        "document.body.dataset.arVisualMode='prepare'",
        "arE7EnsureBaseLayer()",
    ]:
        assert token in block
