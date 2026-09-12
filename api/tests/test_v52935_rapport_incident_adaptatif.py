from pathlib import Path


def html():
    return Path("api/frontend/index.html").read_text(encoding="utf-8")


def test_rapport_incident_et_retour_partagent_un_conteneur_adaptatif():
    s=html()
    assert 'id="ar52934-incident-report"' in s
    assert 'id="ar52934-incident-report"' in s
    assert 'id="ar52-prepare-return"' in s
    assert 'id="ar52-prepare-return"' in s


def test_rapport_visible_et_compact_en_paysage():
    s=html()
    assert '@media (orientation:landscape) and (max-width:1200px)' in s
    assert 'class="ar52936-report-square"' in s
    assert 'width:38px!important;height:38px!important' in s


def test_portrait_evite_le_recouvrement_rapport_retour():
    s=html()
    assert '@media (orientation:portrait) and (max-width:700px)' in s
    assert '.ar52936-return{width:calc(100% - 50px)!important' in s


def test_collecte_automatique_marque_rapport_pret():
    s=html()
    assert 'syncIncidentReportButton' in s
    assert "b.classList.toggle('has-report',ready)" in s
    assert 'content:" · prêt"' in s


def test_stockage_rapport_stable_entre_versions_et_migration_v52934():
    s=html()
    assert "const incidentReportKey='allroads-incident-report';" in s
    assert "allroads-incident-report-v52934" in s


def test_rapport_inclut_identification_vehicule_si_disponible():
    s=html()
    assert "vehicle:vehicle||null" in s
    assert 'Véhicule : ${report.vehicle}' in s
