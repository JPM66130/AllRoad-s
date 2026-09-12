"""Test groupé local : restrictions/alertes par profil + thèmes interface.
Aucun service de routage externe n'est appelé.
"""
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import api.main as main
from db import Base, get_db
from models.restrictions import Restriction
from models.alertes import Alerte

@pytest.mark.restrictions_ui
def test_restrictions_alertes_et_themes_local():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add_all([
        Restriction(type="hauteur", description="Pont 3,8 m", profils_csv="tous", hauteur_limite_m=3.8, niveau="danger"),
        Restriction(type="poids", description="Voie 20 t", profils_csv="bus", poids_limite_t=20.0, niveau="warning"),
        Alerte(titre="Travaux dépôt", message="Accès modifié", profils_csv="bus", niveau="warning"),
    ])
    db.commit(); db.close()

    def override_get_db():
        s = Session()
        try: yield s
        finally: s.close()

    main.app.dependency_overrides[get_db] = override_get_db
    client = TestClient(main.app, client=("127.0.0.1", 50002))
    try:
        access = client.get('/access')
        assert access.status_code == 200
        access_data = access.json()
        assert access_data['state'] == 'TEST'
        assert access_data['service_enabled'] is True
        assert set(access_data['unlocked_profiles']) == {'voiture', 'bus'}
        assert 'poids_lourd' in access_data['visible_profiles']

        # Le verrouillage est côté serveur : un profil grisé ne peut pas contourner l'UI.
        locked_route = client.get('/itineraire/calcul', params={
            'lat1': 42.67, 'lon1': 2.62, 'lat2': 42.68, 'lon2': 2.63, 'profil': 'moto'
        })
        assert locked_route.status_code == 403
        assert locked_route.json()['detail']['code'] == 'PROFILE_LOCKED'

        bus = client.get('/restrictions/profil/bus')
        assert bus.status_code == 200
        data = bus.json()
        assert data['verification_routage'] == 'hgv_beta_non_certifie'
        # Bus standard 4 m -> restriction hauteur 3,8 m déclenchée.
        assert any(r['type'] == 'hauteur' for r in data['restrictions'])
        # 19 t ne dépasse pas la limite 20 t.
        assert not any(r['type'] == 'poids' for r in data['restrictions'])

        voiture = client.get('/restrictions/profil/voiture')
        assert voiture.status_code == 200
        assert voiture.json()['restrictions'] == []
        utilitaire = client.get('/restrictions/profil/utilitaire?hauteur_m=4.10&largeur_m=2.20&longueur_m=7&poids_max_t=3.5')
        assert utilitaire.status_code == 200
        assert any(r['type'] == 'hauteur' for r in utilitaire.json()['restrictions'])
        for profile in ('moto', 'velo', 'pieton', 'camping_car', 'poids_lourd'):
            response = client.get(f'/restrictions/profil/{profile}')
            assert response.status_code == 200

        alerts = client.get('/alertes/profil/bus')
        assert alerts.status_code == 200
        assert len(alerts.json()['alertes']) == 1

        html = Path('api/frontend/index.html').read_text(encoding='utf-8')
        assert 'id="theme-select"' in html
        assert 'keolis-violet' in html and 'keolis-green' in html
        assert 'localStorage.setItem(\'allroads-theme\'' in html
        assert 'refreshVehicleSafety' in html
        assert 'id="ar52815-alert-flash"' in html
        assert 'id="ar52815-mini"' in html
        assert 'AllRoadsAlertRuntime' in html
        assert 'refreshVehicleAlerts' in html
        assert 'restrictionSeverity' in html
        assert 'id="visual-guide"' in html
        assert 'id="visual-guide-arrow"' in html
        assert 'updateVisualGuide' in html
        assert 'routeProgressAt' in html
        assert 'updateGpsGuidance' in html
        assert 'HORS ITINÉRAIRE' in html
        assert 'recalcul sécurisé' in html
        assert 'recalculateFromGps' in html
        assert 'REROUTE_CONFIRM_MS' in html
        assert 'REROUTE_COOLDOWN_MS' in html
        assert 'confirmation avant recalcul' in html
        assert 'id="voice-toggle"' in html
        assert 'speechSynthesis' in html
        assert 'speakGuidance' in html
        assert 'navigationVoiceText' in html
        assert "'critical'" in html
        assert 'FINAL_MANEUVER_M = 50' in html
        assert 'GPS_SAFETY_MAX_M = 35' in html
        assert 'maneuverVoiceStage' in html
        assert "stage = 'final'" in html
        assert 'Dans 200 mètres' in html
        assert 'Dans 500 mètres' in html
        assert 'id="save-vehicle-profile"' in html
        assert 'vehicleStorageKey' in html
        assert 'appendVehicleParams' in html
        assert 'vehicleRestrictionUrl' in html
        assert 'camping_car' in html
        assert 'utilitaire' in html
        assert 'value="moto"' in html
        assert 'value="velo"' in html
        assert 'value="pieton"' in html
        assert "moto: {name:'Ma moto'" in html
        assert "velo: {name:'Mon vélo'" in html
        assert "pieton: {name:'Profil piéton'" in html
        assert 'syncProfileForm' in html
        assert 'id="profile-launcher"' in html
        assert 'is-locked' in html
        assert 'loadAccessRights' in html
        assert 'Bus + Voiture' in html
        assert 'id="field-readiness"' in html
        assert 'updateNetworkReadiness' in html
        assert 'updateGpsReadiness' in html
        assert 'updateRouteEngineReadiness' in html
        assert "window.addEventListener('offline'" in html
        assert 'Mode dégradé' in html
        assert 'userFriendlyError' in html
        assert 'responseError' in html
        assert 'Erreur API (' not in html
        assert 'Recalcul impossible (' not in html
        assert 'Vérifiez la clé ORS' not in html
        assert 'fichier clé.env' not in html
        assert 'error.message;' not in html
        assert 'Ce profil n’est pas encore disponible avec votre accès.' in html
        assert 'Vérifiez que le GPS et l’autorisation de localisation sont activés.' in html
        assert 'gpsStartCheck' in html
        assert '▶ Démarrer la navigation GPS' in html
        assert "if (watchId === null) trackingButton.click();" in html
        assert 'Simulation en cours' in html
        assert 'La navigation GPS est déjà active.' in html
        assert 'id="field-test-panel"' in html
        assert 'startFieldTest' in html
        assert 'stopFieldTest' in html
        assert 'fieldTestSummary' in html
        assert 'allroads-last-field-test' in html
        assert "fieldTestEvent('off_route'" in html
        assert "fieldTestEvent('reroute'" in html
        assert 'Bilan conservé uniquement sur cet appareil.' in html
        assert 'id="tab-btn-tests"' in html
        assert 'id="tab-content-tests"' in html
        assert 'Tests terrain' in html
        assert 'Le GPS s’est-il bien lancé ?' in html
        assert 'L’itinéraire proposé était-il correct ?' in html
        assert 'Instruction trop tardive' in html
        assert 'Tout s’est bien passé' in html
        assert 'saveTestAnswer' in html
        assert 'toggleQuickIssue' in html
        assert 'Réponse enregistrée.' in html
        assert 'Commencez d’abord un essai terrain.' in html
        assert 'id="driving-assistant"' in html
        assert 'Assistant AllRoad’s' in html
        assert 'updateDrivingAssistant' in html
        assert 'Conduite accompagnée' in html
        assert "key:'system:gps'" in html
        assert 'GPS incertain' in html
        assert 'Écart détecté' in html
        assert 'Nouvel itinéraire prêt' in html
        assert 'AllRoad’s vous signalera uniquement ce qui demande votre attention.' in html
        assert 'id="assistant-focus-toggle"' in html
        assert 'allroads-assistant-focus' in html
        assert 'setAssistantFocus' in html
        assert 'assistant-focus' in html
        assert 'assistant-critical' in html
        assert "entry.level === 'critical'" in html
        assert 'speakGuidance(text, priority' in html
        assert 'Les informations essentielles restent prioritaires.' in html
        assert 'id="assistant-priority"' in html
        assert 'id="assistant-action"' in html
        assert 'ACTION MAINTENANT' in html
        assert 'Aucune action nécessaire' in html
        assert 'AllRoad’s conserve l’itinéraire et la dernière position fiable' in html
        assert 'Continuez sur une voie autorisée, sans manœuvre brusque.' in html
        assert 'Courbe serrée · visibilité réduite. Ralentissez et adaptez votre vitesse.' in html
        assert 'id="turnaround-button"' in html
        assert 'Chercher un endroit pour faire demi-tour' in html
        assert 'id="mark-blockage-button"' in html
        assert 'Touchez la route bloquée sur la carte' in html
        assert "apiFetch('/retournement/decouverte-live'" in html
        assert 'Démarrez d’abord le GPS' in html
        assert 'Indiquez d’abord le blocage sur la carte.' in html
        assert 'Zone de retournement proposée' in html
        assert 'id="turnaround-resume"' in html
        assert 'calculateTemporaryTurnaroundRoute' in html
        assert 'resumeOriginalDestination' in html
        assert 'Votre destination initiale est conservée.' in html
        assert 'ZONE SÛRE' in html
        assert 'Destination initiale reprise.' in html
        assert 'id="turnaround-status"' in html
        assert 'showTurnaroundZone' in html
        assert "setTurnaroundStatus('reached', 'zone atteinte')" in html
        assert 'La zone de retournement proposée était-elle adaptée et accessible ?' in html
        assert 'Retournement inadapté' in html
        assert 'turnaround_reached' in html
        assert 'turnaround_resumed' in html
        assert 'id="incident-assistant"' in html
        assert 'id="incident-blockage-button"' in html
        assert 'roadIncidentKind' in html
        assert 'blocking_incident_detected' in html
        assert 'Cette alerte peut bloquer votre trajet.' in html
        assert 'Localisez le blocage sur la carte avant de demander une solution.' in html
        assert 'Blocage signalé · à confirmer' in html
        assert 'Confirmer ce blocage' in html
        assert 'blocking_incident_position_confirmed' in html
        assert 'vous devez la confirmer avant toute recherche de retournement.' in html
        assert 'incidentRelationToRoute' in html
        assert "distanceM <= 80" in html
        assert "distanceM <= 250" in html
        assert "relation.relation === 'outside_route'" in html
        assert 'blocking_incident_ignored' in html
        assert 'Cette alerte se trouve sur votre itinéraire.' in html
        assert 'L’alerte de route bloquée concernait-elle réellement votre itinéraire ?' in html
        assert 'id="mobile-demo-hint"' in html
        assert 'Démo mobile' in html
        demo_launcher = (Path(__file__).resolve().parents[2] / 'DEMO_MOBILE.bat').read_text(encoding='utf-8')
        assert 'ALLROADS_ACCESS_STATE=PRO' in demo_launcher
        assert '8 profils deverrouilles' in demo_launcher
        assert 'Ne tentez pas de demi-tour improvisé.' in html
        assert 'Ne tentez pas de demi-tour improvisé.' in html
        assert '/access' in html
        assert 'class="profile-card-grid"' in html
        for profile in ('pieton','velo','moto','voiture','utilitaire','camping_car','bus','poids_lourd'):
            assert f'data-profile="{profile}"' in html
        assert 'allroads-start-profile' in html
        assert 'open-profile-launcher' in html
        assert 'Un seul AllRoads. Huit façons de voyager.' in html
        assert 'value="poids_lourd"' in html
        assert "poids_lourd: {name:'Mon poids lourd'" in html

        from utils import geo as geo_mod
        from utils.geo import _ors_vehicle_options, ORS_PROFILES, routing_policy
        assert routing_policy('pieton')['preferred'] == 'foot'
        assert routing_policy('velo')['preferred'] == 'bike'
        assert routing_policy('moto')['preferred'] == 'motorcycle'
        assert routing_policy('voiture')['preferred'] == 'car'
        assert routing_policy('bus')['preferred'] == 'hgv'
        assert routing_policy('poids_lourd')['preferred'] == 'hgv'
        assert routing_policy('pieton')['allow_driving_fallback'] is False
        assert routing_policy('velo')['allow_driving_fallback'] is False

        assert ORS_PROFILES['poids_lourd'] == 'driving-hgv'
        assert ORS_PROFILES['bus'] == 'driving-hgv'
        hgv_options = _ors_vehicle_options('poids_lourd', {
            'hauteur_m': 4.0, 'largeur_m': 2.55, 'longueur_m': 16.5, 'poids_max_t': 40.0
        })
        assert hgv_options['vehicle_type'] == 'hgv'
        assert hgv_options['profile_params']['restrictions']['height'] == 4.0
        assert hgv_options['profile_params']['restrictions']['weight'] == 40.0

        # Vérifie localement qu'un piéton/vélo ne bascule jamais silencieusement
        # sur le moteur automobile OSRM si les moteurs adaptés sont indisponibles.
        original_gh = geo_mod._graphhopper_route
        original_ors = geo_mod._ors_client
        original_osrm = geo_mod._osrm_route
        try:
            geo_mod._graphhopper_route = lambda *args, **kwargs: None
            geo_mod._ors_client = lambda: None
            osrm_calls = []
            geo_mod._osrm_route = lambda *args, **kwargs: osrm_calls.append(args) or {
                'distance_km': 1.0, 'duree_min': 1.0, 'source': 'osrm',
                'profil_ors': 'driving'
            }

            pieton_route = geo_mod.calcul_itineraire(42.67, 2.62, 42.68, 2.63, 5, 'pieton')
            assert pieton_route['source'] == 'haversine_fallback'
            assert pieton_route['mode_routage'] == 'estimation_directe'
            assert osrm_calls == []

            voiture_route = geo_mod.calcul_itineraire(42.67, 2.62, 42.68, 2.63, 50, 'voiture')
            assert voiture_route['source'] == 'osrm'
            assert voiture_route['mode_routage'] == 'driving_fallback'
            assert len(osrm_calls) == 1
        finally:
            geo_mod._graphhopper_route = original_gh
            geo_mod._ors_client = original_ors
            geo_mod._osrm_route = original_osrm
    finally:
        main.app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.mark.restrictions_ui
def test_turnaround_rule_blocks_zone_beyond_obstruction():
    client = TestClient(main.app, client=("127.0.0.1", 50003))
    payload = {
        "vehicule": {
            "profil": "bus",
            "hauteur_m": 4.0,
            "largeur_m": 2.55,
            "longueur_m": 18.0,
            "poids_t": 19.0
        },
        "blocage_distance_m": 600,
        "candidats": [
            {
                "id": "beyond",
                "nom": "Rond-point après blocage",
                "type_zone": "rond_point",
                "distance_vehicule_m": 1200,
                "distance_blocage_m": 600,
                "cote_blocage": "apres",
                "confiance_source": 0.95
            },
            {
                "id": "before",
                "nom": "Aire avant blocage",
                "type_zone": "aire",
                "distance_vehicule_m": 250,
                "distance_blocage_m": 600,
                "cote_blocage": "avant",
                "longueur_utile_m": 25,
                "largeur_min_m": 3.0,
                "hauteur_max_m": 4.5,
                "poids_max_t": 30,
                "confiance_source": 0.90
            }
        ]
    }
    response = client.post("/retournement/recherche", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["trouve"] is True
    assert data["proposition"]["id"] == "before"
    rejected = {item["id"]: item["raisons"] for item in data["rejetes"]}
    assert "zone située au-delà du blocage" in rejected["beyond"]


@pytest.mark.restrictions_ui
def test_turnaround_refuses_incompatible_or_unreliable_candidates():
    client = TestClient(main.app, client=("127.0.0.1", 50004))
    payload = {
        "vehicule": {
            "profil": "poids_lourd",
            "hauteur_m": 4.0,
            "largeur_m": 2.55,
            "longueur_m": 16.5,
            "poids_t": 40.0
        },
        "blocage_distance_m": 500,
        "candidats": [
            {
                "id": "too_short",
                "nom": "Petit parking",
                "type_zone": "parking",
                "distance_vehicule_m": 150,
                "distance_blocage_m": 500,
                "cote_blocage": "avant",
                "longueur_utile_m": 10,
                "confiance_source": 0.95
            },
            {
                "id": "uncertain",
                "nom": "Zone incertaine",
                "type_zone": "autre",
                "distance_vehicule_m": 100,
                "distance_blocage_m": 500,
                "cote_blocage": "avant",
                "confiance_source": 0.2
            }
        ]
    }
    response = client.post("/retournement/recherche", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["trouve"] is False
    assert data["proposition"] is None
    assert "Aucune zone de retournement suffisamment fiable" in data["message"]


@pytest.mark.restrictions_ui
def test_turnaround_map_discovery_prefers_reachable_zone():
    client = TestClient(main.app, client=("127.0.0.1", 50005))
    payload = {
        "vehicule": {"profil":"bus","hauteur_m":4.0,"largeur_m":2.55,"longueur_m":18.0,"poids_t":19.0},
        "vehicule_lat": 42.7000, "vehicule_lon": 2.8900,
        "blocage_lat": 42.7054, "blocage_lon": 2.8900,
        "blocage_distance_m": 600,
        "zones": [
            {"id":"safe","nom":"Rond-point accessible","latitude":42.7022,"longitude":2.8900,
             "type_zone":"rond_point","longueur_utile_m":25,"poids_max_t":30,"confiance_source":0.9},
            {"id":"beyond","nom":"Aire après accident","latitude":42.7108,"longitude":2.8900,
             "type_zone":"aire","longueur_utile_m":30,"poids_max_t":40,"confiance_source":0.95}
        ]
    }
    r=client.post("/retournement/decouverte-carte",json=payload)
    assert r.status_code == 200
    d=r.json()
    assert d["trouve"] is True
    assert d["proposition"]["id"] == "safe"
    assert d["zones_analysees"] == 2
    rejected={x["id"]:x["raisons"] for x in d["rejetes"]}
    assert "zone située au-delà du blocage" in rejected["beyond"]


@pytest.mark.restrictions_ui
def test_turnaround_map_discovery_can_return_no_solution():
    client = TestClient(main.app, client=("127.0.0.1", 50006))
    payload = {
        "vehicule": {"profil":"poids_lourd","hauteur_m":4.0,"largeur_m":2.55,"longueur_m":16.5,"poids_t":40.0},
        "vehicule_lat":42.7000,"vehicule_lon":2.8900,
        "blocage_lat":42.7045,"blocage_lon":2.8900,"blocage_distance_m":500,
        "zones":[
            {"id":"small","nom":"Petit parking","latitude":42.7010,"longitude":2.8900,
             "type_zone":"parking","longueur_utile_m":9,"poids_max_t":3.5,"confiance_source":0.95}
        ]
    }
    d=client.post("/retournement/decouverte-carte",json=payload).json()
    assert d["trouve"] is False
    assert d["proposition"] is None
    assert "Ne tentez pas de demi-tour improvisé" in d["action"]


@pytest.mark.restrictions_ui
def test_turnaround_live_uses_real_map_layer_without_external_call(monkeypatch):
    from routers import turnaround as tr

    async def fake_fetch(lat, lon, radius):
        return [
            {
                "id":"osm-way-1","nom":"Rond-point test","latitude":42.7020,"longitude":2.8900,
                "type_zone":"rond_point","prive":False,"accessible":True,
                "hauteur_max_m":None,"largeur_min_m":None,"longueur_utile_m":25.0,
                "poids_max_t":30.0,"confiance_source":0.78
            },
            {
                "id":"osm-way-2","nom":"Parking après blocage","latitude":42.7100,"longitude":2.8900,
                "type_zone":"parking","prive":False,"accessible":True,
                "hauteur_max_m":None,"largeur_min_m":None,"longueur_utile_m":30.0,
                "poids_max_t":30.0,"confiance_source":0.8
            }
        ]

    monkeypatch.setattr(tr, "_fetch_overpass_zones", fake_fetch)
    client = TestClient(main.app, client=("127.0.0.1", 50007))
    payload = {
        "vehicule":{"profil":"bus","hauteur_m":4.0,"largeur_m":2.55,"longueur_m":18.0,"poids_t":19.0},
        "vehicule_lat":42.7000,"vehicule_lon":2.8900,
        "blocage_lat":42.7054,"blocage_lon":2.8900,"blocage_distance_m":600,"rayon_m":1200
    }
    r=client.post("/retournement/decouverte-live",json=payload)
    assert r.status_code == 200
    d=r.json()
    assert d["trouve"] is True
    assert d["proposition"]["id"] == "osm-way-1"
    assert d["proposition"]["latitude"] == 42.702
    assert d["proposition"]["longitude"] == 2.89
    assert d["source"] == "OpenStreetMap"


@pytest.mark.restrictions_ui
def test_turnaround_live_fails_safely_when_map_source_unavailable(monkeypatch):
    from routers import turnaround as tr
    import httpx

    async def fake_fail(lat, lon, radius):
        raise httpx.ConnectError("offline")

    monkeypatch.setattr(tr, "_fetch_overpass_zones", fake_fail)
    client = TestClient(main.app, client=("127.0.0.1", 50008))
    payload = {
        "vehicule":{"profil":"camping_car","hauteur_m":3.2,"largeur_m":2.35,"longueur_m":7.5,"poids_t":3.5},
        "vehicule_lat":42.7000,"vehicule_lon":2.8900,
        "blocage_lat":42.7040,"blocage_lon":2.8900,"blocage_distance_m":450
    }
    d=client.post("/retournement/decouverte-live",json=payload).json()
    assert d["trouve"] is False
    assert d["source"] == "indisponible"
    assert "Ne tentez pas de demi-tour improvisé" in d["action"]

@pytest.mark.restrictions_ui
def test_turnaround_route_guard_accepts_route_away_from_blockage():
    from routers.itineraires import geometry_min_distance_to_point_m
    geometry = {"type":"LineString","coordinates":[[2.8800,42.7000],[2.8810,42.7010],[2.8820,42.7020]]}
    distance = geometry_min_distance_to_point_m(geometry, 42.7050, 2.8900)
    assert distance is not None
    assert distance > 60


@pytest.mark.restrictions_ui
def test_turnaround_route_guard_rejects_crossing_segment_even_if_vertices_are_far():
    from routers.itineraires import geometry_min_distance_to_point_m
    # Le segment traverse exactement le blocage, alors que les deux sommets sont à plusieurs centaines de mètres.
    geometry = {"type":"LineString","coordinates":[[2.8800,42.7000],[2.9000,42.7000]]}
    distance = geometry_min_distance_to_point_m(geometry, 42.7000, 2.8900)
    assert distance is not None
    assert distance < 1


@pytest.mark.restrictions_ui
def test_turnaround_route_guard_detects_near_radius():
    from routers.itineraires import geometry_min_distance_to_point_m
    geometry = {"type":"LineString","coordinates":[[2.8800,42.70045],[2.9000,42.70045]]}
    distance = geometry_min_distance_to_point_m(geometry, 42.7000, 2.8900)
    assert distance is not None
    assert 40 <= distance <= 60


@pytest.mark.restrictions_ui
def test_v51_mobile_map_block_is_present_and_turnaround_requests_avoidance():
    html = Path(__file__).resolve().parents[1] / 'frontend' / 'index.html'
    text = html.read_text(encoding='utf-8')
    assert 'allroads-v51-mobile-map-script' in text
    assert 'Préparer le trajet' in text
    assert 'Démo sans GPS' in text
    assert "params.set('avoid_lat', blockagePoint.lat)" in text
    assert "params.set('avoid_lon', blockagePoint.lon)" in text
    assert "params.set('avoid_radius_m'" in text
    assert 'passe trop près du blocage' in text

@pytest.mark.restrictions_ui
def test_v52_vehicle_garage_is_between_home_and_map():
    html = Path(__file__).resolve().parents[1] / 'frontend' / 'index.html'
    text = html.read_text(encoding='utf-8')
    assert 'allroads-v52-vehicle-script' in text
    assert 'Quel véhicule conduisez-vous ?' in text
    assert 'AllRoadsVehicleGarage.open(normalized)' in text
    assert "AllRoadsMobileNav.open(profile)" in text

@pytest.mark.restrictions_ui
def test_v52_supports_five_saved_vehicles_default_and_temporary():
    html = Path(__file__).resolve().parents[1] / 'frontend' / 'index.html'
    text = html.read_text(encoding='utf-8')
    assert 'v.slice(0,5)' in text
    assert '5 véhicules enregistrés' in text
    assert 'Véhicule occasionnel' in text
    assert 'par défaut' in text

@pytest.mark.restrictions_ui
def test_v52_selected_dimensions_feed_legacy_route_fields():
    html = Path(__file__).resolve().parents[1] / 'frontend' / 'index.html'
    text = html.read_text(encoding='utf-8')
    for field in ('hauteur_m','largeur_m','longueur_m','poids_max_t','vitesse_max_kmh','consommation'):
        assert f"set('{field}'" in text
