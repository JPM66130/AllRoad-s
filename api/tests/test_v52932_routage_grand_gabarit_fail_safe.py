from pathlib import Path

from routers.itineraires import routing_assurance


def test_bus_secours_auto_ne_peut_pas_etre_presente_comme_gabarit_garanti():
    assurance = routing_assurance(
        "bus",
        {"source": "osrm_fallback", "profil_ors": "driving-car", "mode_routage": "driving_fallback"},
    )
    assert assurance["guidage_autorise"] is False
    assert assurance["gabarit_verifie_moteur"] is False
    assert assurance["niveau_garantie_routage"] == "informatif_non_garanti"
    assert "guidage réel reste bloqué" in assurance["message_securite_routage"]


def test_bus_ors_hgv_autorise_le_guidage_avec_garde_fou():
    assurance = routing_assurance(
        "bus",
        {"source": "openrouteservice", "profil_ors": "driving-hgv", "mode_routage": "hgv"},
    )
    assert assurance["guidage_autorise"] is True
    assert assurance["gabarit_verifie_moteur"] is True
    assert assurance["niveau_garantie_routage"] == "hgv_moteur_verifie"


def test_voiture_reste_autorisee_sur_secours_auto():
    assurance = routing_assurance(
        "voiture",
        {"source": "osrm_fallback", "profil_ors": "driving-car", "mode_routage": "driving_fallback"},
    )
    assert assurance["guidage_autorise"] is True
    assert assurance["gabarit_verifie_moteur"] is None


def test_interface_bloque_techniquement_le_demarrage_si_gabarit_non_garanti():
    html = Path("api/frontend/index.html").read_text(encoding="utf-8")
    assert "lastCalculatedData.guidage_autorise === false" in html
    assert "Guidage grand gabarit bloqué" in html
    assert "mapNavLaunchBtn.disabled = blockedByGabarit" in html
    assert "NON GARANTI" in html


def test_lanceur_utilise_la_version_courante_pour_casser_le_cache():
    launchers = sorted(Path(".").glob('*LANCER_ALLROADS_V52_9_*.bat'))
    assert len(launchers) == 1
    launcher = launchers[0].read_text(encoding="utf-8")
    assert "V52.9.102" in launcher
    assert "?v=52.9.100" in launcher
    assert "?v=52.9.29" not in launcher
