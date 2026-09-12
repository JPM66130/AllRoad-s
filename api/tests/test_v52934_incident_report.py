from pathlib import Path
HTML=Path(__file__).resolve().parents[1]/"frontend"/"index.html"
def src(): return HTML.read_text(encoding="utf-8")
def test_small_incident_report_button_and_stop_message():
 s=src(); assert 'id="ar52934-incident-report"' in s; assert 'Rapport d’incident' in s; assert 'véhicule à l’arrêt' in s
def test_incident_report_is_independent_from_field_test():
 s=src(); assert "const incidentReportKey='allroads-incident-report'" in s; assert 'function incidentReportEvent' in s
def test_incident_flow_feeds_report():
 s=src()
 for e in ('blockage_reported','turnaround_search','turnaround_guidance_started','turnaround_reached','route_recalculated','turnaround_cancelled'):
  assert f"incidentReportEvent('{e}'" in s
def test_client_copy_not_falsely_claimed_active():
 s=src(); assert 'Envoi externe non activé dans cette version de démonstration.' in s
def test_no_unsafe_revenez_sur_vos_pas(): assert 'revenez sur vos pas' not in src().lower()

def test_report_button_respects_important_action_lock(): assert "'#ar52934-incident-report'" in src()
