from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend/index.html').read_text(encoding='utf-8')

def test_route_edit_has_explicit_validate_button():
    assert 'id="vsflat-route-validate"' in HTML
    assert '>Valider</button>' in HTML
    assert 'validate.onclick=confirmActiveEdit' in HTML

def test_android_enter_uses_same_validation_path():
    assert "if(e.key!=='Enter')return" in HTML
    assert 'confirmActiveEdit()' in HTML

def test_call_buttons_stay_above_open_panel():
    assert '#vsflat-vehicle-row{position:relative!important;z-index:110!important}' in HTML
    assert 'position:absolute!important;z-index:100!important;top:var(--vs-panel-anchor)!important' in HTML

def test_hidden_controls_really_disappear():
    assert '.vsflat-action[hidden]{display:none!important}' in HTML
    assert "if(p==='PIETON')return 'none'" in HTML

def test_light_pro_profiles_are_supported_without_heavy_dimensions():
    assert "if(['VELO','MOTO'].includes(p))return 'light'" in HTML
    assert "function supportsTours(p=profile()){return ['VELO','MOTO','BUS'].includes(p)}" in HTML
    assert 'Profil professionnel léger · ID facultatif' in HTML
