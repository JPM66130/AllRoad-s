from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HTML=(ROOT/'frontend/index.html').read_text(encoding='utf-8')

def test_panel_anchor_is_half_real_button_row_height():
    assert "Math.round(h/2)" in HTML
    assert "--vs-panel-anchor" in HTML
    assert "top:var(--vs-panel-anchor)!important" in HTML

def test_itinerary_uses_real_input_not_whole_card_overlay():
    assert "body.vsflat-editing-route input.vsflat-active-input" in HTML
    assert "body.vsflat-editing:not(.vsflat-editing-panel) #vsflat-route-card{" not in HTML

def test_enter_validates_active_business_form():
    assert "if(e.key!=='Enter')return" in HTML
    assert "#vsflat-v-save,#vsflat-tour-save" in HTML
    assert "setTimeout(()=>save.click(),0)" in HTML

def test_landscape_keyboard_uses_visual_viewport_only_during_edit():
    assert "window.visualViewport?.addEventListener('resize'" in HTML
    assert "if(activeEdit)syncEditViewport()" in HTML
    assert "--vs-edit-height" in HTML

def test_pedestrian_has_no_vehicle_business_controls_by_default():
    assert "['VOITURE','UTILITAIRE','CAMPING_CAR','BUS','POIDS_LOURD'].includes(p)" in HTML
