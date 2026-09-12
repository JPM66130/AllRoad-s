from pathlib import Path

HTML = Path('api/frontend/index.html').read_text(encoding='utf-8')


def test_e3_une_seule_autorite_gps_exposee_aux_vues():
    assert "window.AllRoadsGpsRuntime =" in HTML
    assert "start: startRealGpsTracking" in HTML
    assert "stop: stopRealGpsTracking" in HTML
    # Un seul abonnement GPS continu dans la page : l'autorité centrale.
    assert HTML.count("navigator.geolocation.watchPosition(") == 1


def test_e3_demarrage_mobile_normal_lance_le_gps_reel():
    assert "const started=window.AllRoadsGpsRuntime?.start();" in HTML
    assert "Deux chemins explicites seulement" in HTML
    assert "if(demoMode){" in HTML
    assert "window.AllRoadsGpsRuntime?.stop('switch-to-simulation');" in HTML
    assert "if(!routeLayer){driveStartRequested=false;toast('Simulation indisponible : calculez d’abord un itinéraire réel.');return false;}" in HTML


def test_e3_mouvement_ne_bouge_pas_sans_source_explicite():
    assert "motion={mode:'idle',speedKmh:0,progress:0}" in HTML
    assert "motion.mode==='idle'?0" in HTML
    assert "setRealSpeed(speedKmh" in HTML
    assert "setSimulationSpeed(speedKmh" in HTML
    assert "):58;" not in HTML


def test_e3_vitesse_reelle_a_une_seule_fonction_de_publication():
    assert "function publishRealDrivingSpeed(speedKmh" in HTML
    assert "window.AllRoadsSpeed67?.setSpeed(value);" in HTML
    assert "window.AllRoadsDriveMotion?.setRealSpeed(value ?? 0, progress);" in HTML
    assert "document.getElementById('driver-speed').textContent = `${Math.round(gpsSpeedKmh)} km/h`;" not in HTML


def test_e3_gps_incertain_et_perdu_restent_fail_safe():
    assert "GPS_UNCERTAIN_ACCURACY_M = 50" in HTML
    assert "GPS_LOST_AFTER_MS = 15000" in HTML
    assert "const guidancePosition = reliable ? position : lastReliablePosition" in HTML
    assert "GPS INCERTAIN" in HTML
    assert "GPS INDISPONIBLE" in HTML
    assert "publishRealDrivingSpeed(null, 0, 'lost');" in HTML
    assert "publishRealDrivingSpeed(null, 0, 'error');" in HTML


def test_e3_vitesse_android_sans_coords_speed_a_un_secours_gps_reel():
    assert "function speedFromReliableFix(position)" in HTML
    assert "source = 'coords.speed'" in HTML
    assert "source = speedKmh === null ? 'unavailable' : 'gps-delta'" in HTML
    assert "gpsDistanceKm(lastSpeedFixPosition, position)" in HTML


def test_e3_etat_attente_ne_se_fait_pas_passer_pour_zero_kmh():
    assert "GPS EN ATTENTE" in HTML
    assert "publishRealDrivingSpeed(null, 0, 'waiting')" in HTML
    assert "value === null ? '-- km/h'" in HTML


def test_e3_vitesse_simulation_passe_par_une_autorite_identifiee():
    assert "window.AllRoadsDrivingSpeed =" in HTML
    assert "simulation: publishSimulationDrivingSpeed" in HTML
    assert "window.AllRoadsDrivingSpeed?.simulation(samples[i])" in HTML

def test_e3_demarrage_n_attend_pas_le_premier_fix_gps():
    assert "GPS EN ATTENTE" in HTML
    assert "watchId = openNativeGpsWatch" in HTML
    assert HTML.count("navigator.geolocation.watchPosition(") == 1
    assert "Le GPS réel doit être disponible pour démarrer la conduite." not in HTML
    assert "getStartIssue: () => lastGpsStartIssue" in HTML


def test_e3_gps_non_supporte_ouvre_sans_mouvement_invente():
    assert "GPS indisponible sur cet appareil. La conduite reste ouverte sans mouvement inventé." in HTML
    assert "publishRealDrivingSpeed(null, 0, 'unsupported')" in HTML


def test_e3_blocage_securite_routage_reste_distinct_du_gps():
    assert "reason:'routing-safety'" in HTML
    assert "Guidage grand gabarit bloqué" in HTML



def test_e3_indicateur_reception_gps_visible_et_lie_a_la_precision():
    assert 'id="ar-e3-gps-signal"' in HTML
    assert "function updateGpsSignalIndicator" in HTML
    assert "E3 — indicateur GPS compact intégré à la barre haute" in HTML
    header = HTML[HTML.index('<header class="ar51-topbar">'):HTML.index('</header>', HTML.index('<header class="ar51-topbar">'))]
    assert 'id="ar-e3-gps-signal"' in header
    assert 'class="ar-e3-gps-bars"' in HTML
    assert "data-level=\"0\"" in HTML
    assert "level='4'" in HTML
    assert "INDISPONIBLE" in HTML
    assert "updateGpsSignalIndicator('reliable', accuracy)" in HTML
    assert "updateGpsSignalIndicator('uncertain', accuracy)" in HTML


def test_e3_diagnostic_geolocation_expose_le_code_navigateur_sans_deuxieme_watch():
    assert "function gpsErrorLabel(code)" in HTML
    assert "if (code === 1) return 'AUTORISATION'" in HTML
    assert "if (code === 2) return 'POSITION'" in HTML
    assert "if (code === 3) return 'DÉLAI'" in HTML
    assert "}, error => {" in HTML
    assert "Diagnostic GPS : E${code || '?'} ${label}" in HTML
    assert "getDiagnostic: () => ({...lastGpsDiagnostic})" in HTML
    assert HTML.count("navigator.geolocation.watchPosition(") == 1
