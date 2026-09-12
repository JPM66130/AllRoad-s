from pathlib import Path

HTML = (Path(__file__).parents[1] / "frontend" / "index.html").read_text(encoding="utf-8")


def test_e5_has_single_alert_runtime_and_product_priority():
    assert HTML.count("const AllRoadsAlertRuntime = (() => {") == 1
    assert "const priorityRank = { danger: 4, safety: 3, navigation: 2, info: 1 };" in HTML
    assert "window.AllRoadsAlertRuntime = AllRoadsAlertRuntime;" in HTML


def test_e5_has_one_visible_alert_surface_and_no_legacy_renderer():
    assert HTML.count('id="ar52815-alert-flash"') == 1
    assert HTML.count('id="ar52815-mini"') == 1
    assert 'id="driver-alert-panel"' not in HTML
    assert 'id="map-alert-strip"' not in HTML
    assert "function ar52815Alert(" not in HTML
    assert "function ar52815ShowMini(" not in HTML


def test_e5_voice_is_capped_at_three_and_has_no_timer_loop():
    assert "const MAX_VOICE_MESSAGES = 3;" in HTML
    assert "previous.count >= MAX_VOICE_MESSAGES" in HTML
    assert "armReminder(" not in HTML
    assert "reminderTimer" not in HTML


def test_e5_road_alerts_use_authoritative_queue():
    assert "AllRoadsAlertRuntime.replaceSource('road', entries);" in HTML
    assert "AllRoadsAlertRuntime.replaceSource('road', []);" in HTML


def test_e5_simulated_danger_uses_distance_voice_and_one_end_message():
    assert HTML.count("key:'simulation:virage',category:'danger',level:'critical',voiceMode:'distance'") == 1
    assert "'Attention, virage dangereux dans 300 mètres.','300m'" in HTML
    assert "'Virage dangereux dans 100 mètres.','100m'" in HTML
    assert "'Virage dangereux.','entree'" in HTML
    assert "{endVoice:'Fin de la zone dangereuse.'}" in HTML
    assert "window.AllRoadsAlertRuntime?.resolve('simulation:virage')" in HTML
    assert "ar52815Alert('Virage dangereux'" not in HTML


def test_e5_legacy_sector_scenario_is_not_started_by_generic_demo():
    start = HTML.split('function startDriving(){',1)[1].split('function open(p)',1)[0]
    assert 'arJ232StartRouteSimulation()' in start
    assert 'ar5287Start' not in start
    assert "ar5287Event=10;ar5287ApplyEvent(10);" in HTML
    assert "if(idx===10)" in HTML
