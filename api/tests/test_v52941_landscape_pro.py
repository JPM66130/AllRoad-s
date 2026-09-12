from pathlib import Path

HTML = (Path(__file__).resolve().parents[1] / "frontend" / "index.html").read_text(encoding="utf-8")


def test_v52941_landscape_style_present():
    assert 'id="allroads-v52941-landscape-pro"' in HTML
    assert 'V52.9.102' in HTML


def test_home_landscape_uses_cover_not_squash():
    block = HTML.split('id="allroads-v52941-landscape-pro"', 1)[1].split('</style>', 1)[0]
    assert 'grid-template-columns:repeat(4,minmax(0,1fr))' in block
    assert 'object-fit:cover!important' in block
    assert '.ar-profile-copy{' in block
    assert 'position:absolute!important' in block


def test_vehicle_landscape_has_fixed_zones():
    block = HTML.split('id="allroads-v52941-landscape-pro"', 1)[1].split('</style>', 1)[0]
    assert 'grid-template-rows:38px 33px minmax(0,1fr) 36px 44px' in block
    assert '.ar52-title h1' in block
    assert '.ar52-profile' in block


def test_prepare_landscape_is_compact_and_complete():
    block = HTML.split('id="allroads-v52941-landscape-pro"', 1)[1].split('</style>', 1)[0]
    assert 'height:104px!important;max-height:104px!important' in block
    assert '.ar52-tripmode' in block
    assert '.ar51-route-fields' in block
    assert '.ar526-prepare-actions' in block


def test_reference_views_not_overridden_by_v52941():
    block = HTML.split('id="allroads-v52941-landscape-pro"', 1)[1].split('</style>', 1)[0]
    assert '[data-state="ready"]' not in block
    assert '[data-state="driving"]' not in block
