from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / 'frontend' / 'index.html'

def source():
    return HTML.read_text(encoding='utf-8')

def test_incident_actions_feed_field_report():
    s=source()
    for event in ('blockage_reported','turnaround_search','turnaround_guidance_started','turnaround_reached','route_recalculated','turnaround_cancelled'):
        assert f"fieldTestEvent('{event}'" in s

def test_recalculated_report_explicitly_records_blockage_exclusion():
    assert "fieldTestEvent('route_recalculated', 'Blocage exclu du trajet recalculé')" in source()

def test_no_unsafe_revenez_sur_vos_pas():
    assert 'revenez sur vos pas' not in source().lower()
