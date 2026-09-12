from pathlib import Path

HTML = Path("api/frontend/index.html").read_text(encoding="utf-8")

def test_v52956_bandeau_sous_coque_et_commandes_hautes():
    assert 'id="allroads-v52956-guidage-sous-coque"' in HTML
    block = HTML.split('id="allroads-v52956-guidage-sous-coque"',1)[1].split('</style>',1)[0]
    assert '+ 112px' in block
    assert '+ 180px' in block
    assert '.ar525-mapviews' in block
    assert '.ar51-center-map' in block

def test_v52956_frontends_identiques():
    assert Path("frontend/index.html").read_bytes() == Path("api/frontend/index.html").read_bytes()

def test_v52956_lanceur_court_et_versionne():
    p=Path("AA_LANCER_JEPALYS.bat")
    assert p.exists()
    assert b"52.9.100" in p.read_bytes()
