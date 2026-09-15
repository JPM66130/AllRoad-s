import math
import logging
import os
import json
import urllib.parse
import urllib.request

from dotenv import load_dotenv

try:
    import openrouteservice
except ImportError:
    openrouteservice = None


logger = logging.getLogger(__name__)


class GeocodingUnavailable(RuntimeError):
    """Le fournisseur de géocodage n’a pas répondu correctement."""


ORS_PROFILES = {
    "voiture": "driving-car",
    "moto": "driving-car",
    "velo": "cycling-regular",
    "pieton": "foot-walking",
    "bus": "driving-hgv",
    "utilitaire": "driving-hgv",
    "camping_car": "driving-hgv",
    "poids_lourd": "driving-hgv",
}

GRAPHHOPPER_VEHICLES = {
    "voiture": "car",
    "moto": "motorcycle",
    "velo": "bike",
    "pieton": "foot",
    "bus": "car",
    "utilitaire": "car",
    "camping_car": "car",
    "poids_lourd": "truck",
}


ROUTING_POLICIES = {
    "pieton": {
        "label": "Piéton",
        "preferred": "foot",
        "allow_driving_fallback": False,
        "heavy": False,
    },
    "velo": {
        "label": "Vélo",
        "preferred": "bike",
        "allow_driving_fallback": False,
        "heavy": False,
    },
    "moto": {
        "label": "Moto",
        "preferred": "motorcycle",
        "allow_driving_fallback": True,
        "heavy": False,
    },
    "voiture": {
        "label": "Voiture",
        "preferred": "car",
        "allow_driving_fallback": True,
        "heavy": False,
    },
    "utilitaire": {
        "label": "Utilitaire",
        "preferred": "hgv",
        "allow_driving_fallback": True,
        "heavy": True,
    },
    "camping_car": {
        "label": "Camping-car",
        "preferred": "hgv",
        "allow_driving_fallback": True,
        "heavy": True,
    },
    "bus": {
        "label": "Bus",
        "preferred": "hgv",
        "allow_driving_fallback": True,
        "heavy": True,
    },
    "poids_lourd": {
        "label": "Poids lourd",
        "preferred": "hgv",
        "allow_driving_fallback": True,
        "heavy": True,
    },
}


def routing_policy(profil):
    return ROUTING_POLICIES.get(profil, ROUTING_POLICIES["voiture"])

FERRY_ROUTES = [
    {"nom": "Calais - Douvres", "depart": [50.966, 1.862], "arrivee": [51.127, 1.313], "duree_min": 90, "prix_eur": 180},
    {"nom": "Barcelone - Tanger Med", "depart": [41.34, 2.17], "arrivee": [35.88, -5.5], "duree_min": 900, "prix_eur": 350},
    {"nom": "Algeciras - Tanger Med", "depart": [36.13, -5.45], "arrivee": [35.88, -5.5], "duree_min": 90, "prix_eur": 150},
    {"nom": "Gênes - Palerme", "depart": [44.41, 8.93], "arrivee": [38.12, 13.36], "duree_min": 1200, "prix_eur": 300},
]


def liaisons_ferry():
    return FERRY_ROUTES


def _read_env_value(env_path, key_name):
    if not os.path.isfile(env_path):
        return None
    with open(env_path, encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            candidate_key, candidate_value = line.split("=", 1)
            if candidate_key.strip() == key_name:
                return candidate_value.strip()
    return None


def _secret_env_paths():
    """Retourne les emplacements historiques possibles du fichier de clés sans rien renommer.

    Certains ZIP Windows ont conservé le nom encodé ``cl#U00e9.env`` au lieu de
    ``clé.env``. On accepte les deux afin que le routage reste portable et stable.
    """
    api_dir = os.path.dirname(os.path.dirname(__file__))
    return [
        os.path.join(api_dir, "clé.env"),
        os.path.join(api_dir, "cl#U00e9.env"),
    ]


def _secret_value(key_name):
    # Les variables d'environnement restent prioritaires en production.
    value = os.getenv(key_name)
    if value:
        return value
    for env_path in _secret_env_paths():
        if not os.path.isfile(env_path):
            continue
        load_dotenv(env_path, override=False)
        value = os.getenv(key_name) or _read_env_value(env_path, key_name)
        if value:
            return value
    return None


def _ors_api_key():
    api_key = _secret_value("ORS_API_KEY")
    if not api_key:
        return None
    placeholder_markers = ("VOTRE_", "YOUR_", "CHANGE_ME", "CHANGEME", "EXAMPLE")
    if api_key.upper().startswith(placeholder_markers):
        logger.warning("Clé ORS non configurée ou placeholder détectée; géocodage désactivé.")
        return None
    return api_key


def _ors_client():
    if openrouteservice is None:
        return None

    api_key = _ors_api_key()
    if not api_key:
        return None
    return openrouteservice.Client(key=api_key, base_url="https://api.heigit.org/openrouteservice")


def _graphhopper_api_key():
    api_key = _secret_value("GRAPHOPPER_API_KEY")
    if not api_key or api_key.upper().startswith(("VOTRE_", "YOUR_", "CHANGE_ME", "EXAMPLE", "REMPLACEZ_")):
        return None
    return api_key


def _graphhopper_route(lat1, lon1, lat2, lon2, profil, preference=None):
    api_key = _graphhopper_api_key()
    if api_key is None:
        return None

    query = urllib.parse.urlencode(
        [
            ("point", f"{lat1},{lon1}"),
            ("point", f"{lat2},{lon2}"),
            ("vehicle", GRAPHHOPPER_VEHICLES.get(profil, "car")),
            ("locale", "fr"),
            ("instructions", "true"),
            ("points_encoded", "false"),
            *(([("algorithm", "alternative_route")] if preference == "alternative" else [])),
            ("key", api_key),
        ]
    )
    url = f"https://graphhopper.com/api/1/route?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": "AllRoads/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))

    paths = payload.get("paths", [])
    if not paths:
        raise RuntimeError("GraphHopper ne propose pas de route")
    selected = paths[0]
    return {
        "distance_km": round(selected["distance"] / 1000, 2),
        "duree_min": round(selected["time"] / 60000, 1),
        "source": "graphhopper",
        "profil_ors": GRAPHHOPPER_VEHICLES.get(profil, "car"),
        "steps": [
            {
                "instruction": instruction.get("text", "Continuer"),
                "distance_km": round(instruction.get("distance", 0) / 1000, 2),
                "duree_min": round(instruction.get("time", 0) / 60000, 1),
            }
            for instruction in selected.get("instructions", [])
        ],
        "geometry": selected["points"],
    }

def distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcule la distance en kilomètres entre deux points GPS.
    Formule de Haversine.
    """
    R = 6371  # Rayon de la Terre en km

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def duree_minutes(distance_km: float, vitesse_kmh: float = 70) -> float:
    """
    Calcule la durée estimée en minutes.
    Par défaut : 70 km/h (camping-car C25).
    """
    if vitesse_kmh <= 0:
        return 0
    heures = distance_km / vitesse_kmh
    return heures * 60


def _osrm_route(lat1, lon1, lat2, lon2):
    coordinates = f"{lon1},{lat1};{lon2},{lat2}"
    query = urllib.parse.urlencode({"overview": "full", "geometries": "geojson", "steps": "true"})
    url = f"https://router.project-osrm.org/route/v1/driving/{coordinates}?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": "AllRoads/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        route = json.loads(response.read().decode("utf-8"))
    if route.get("code") != "Ok" or not route.get("routes"):
        raise RuntimeError("OSRM ne propose pas de route")
    selected = route["routes"][0]
    steps = [
        {
            "instruction": step.get("name") or step.get("maneuver", {}).get("type", "Continuer"),
            "distance_km": round(step.get("distance", 0) / 1000, 2),
            "duree_min": round(step.get("duration", 0) / 60, 1),
        }
        for leg in selected.get("legs", [])
        for step in leg.get("steps", [])
    ]
    return {
        "distance_km": round(selected["distance"] / 1000, 2),
        "duree_min": round(selected["duration"] / 60, 1),
        "source": "osrm_fallback",
        "profil_ors": "driving-car",
        "steps": steps,
        "geometry": selected["geometry"],
    }


def _route_routiere(client, start, end, profile, options=None):
    kwargs = {
        "coordinates": [[start[1], start[0]], [end[1], end[0]]],
        "profile": profile,
        "format": "geojson",
    }
    if options:
        kwargs["options"] = options
    route = client.directions(**kwargs)
    feature = route["features"][0]
    summary = feature["properties"]["summary"]
    steps = []
    for segment in feature["properties"].get("segments", []):
        for step in segment.get("steps", []):
            steps.append({
                "instruction": step.get("instruction", ""),
                "distance_km": round(step.get("distance", 0) / 1000, 2),
                "duree_min": round(step.get("duration", 0) / 60, 1),
            })
    return summary, feature["geometry"], steps


def geocoder(adresse, focus_lat=None, focus_lon=None):
    api_key = _ors_api_key()
    if api_key is None:
        return []
    params = {"text": adresse, "size": 10}
    if focus_lat is not None and focus_lon is not None:
        params["focus.point.lat"] = float(focus_lat)
        params["focus.point.lon"] = float(focus_lon)
    query = urllib.parse.urlencode(params)
    request = urllib.request.Request(
        f"https://api.heigit.org/pelias/v1/search?{query}",
        headers={"Authorization": api_key, "User-Agent": "AllRoads/1.0"},
    )
    response = None
    last_error = None
    # Une panne réseau ponctuelle ne doit jamais être transformée en « adresse introuvable ».
    # Deux essais utilisent exactement le même fournisseur et la même requête.
    for attempt in range(2):
        try:
            with urllib.request.urlopen(request, timeout=20) as raw_response:
                response = json.loads(raw_response.read().decode("utf-8"))
            break
        except Exception as error:
            last_error = error
            logger.warning("Geocodage ORS indisponible (essai %s/2): %s", attempt + 1, error)
    if response is None:
        raise GeocodingUnavailable("Service de recherche d’adresse temporairement indisponible") from last_error
    places = [
        {
            "nom": feature.get("properties", {}).get("label", adresse),
            "pays": feature.get("properties", {}).get("country"),
            "longitude": feature["geometry"]["coordinates"][0],
            "latitude": feature["geometry"]["coordinates"][1],
        }
        for feature in response.get("features", [])[:10]
    ]
    # Le focus Pelias n'est qu'une préférence : AllRoad's classe lui-même
    # les homonymes par proximité du départ réellement résolu.
    if focus_lat is not None and focus_lon is not None:
        places.sort(key=lambda place: distance_km(float(focus_lat), float(focus_lon), float(place["latitude"]), float(place["longitude"])))
    return places[:5]


def reverse_geocoder(latitude, longitude):
    api_key = _ors_api_key()
    if api_key is None:
        return None
    params = {"point.lat": float(latitude), "point.lon": float(longitude), "size": 1}
    query = urllib.parse.urlencode(params)
    request = urllib.request.Request(
        f"https://api.heigit.org/pelias/v1/reverse?{query}",
        headers={"Authorization": api_key, "User-Agent": "AllRoads/1.0"},
    )
    response = None
    last_error = None
    for attempt in range(2):
        try:
            with urllib.request.urlopen(request, timeout=20) as raw_response:
                response = json.loads(raw_response.read().decode("utf-8"))
            break
        except Exception as error:
            last_error = error
            logger.warning("Geocodage inverse ORS indisponible (essai %s/2): %s", attempt + 1, error)
    if response is None:
        raise GeocodingUnavailable("Service de geocodage inverse temporairement indisponible") from last_error
    features = response.get("features", [])
    if not features:
        return None
    feature = features[0]
    properties = feature.get("properties", {})
    return {
        "nom": properties.get("label") or "Position GPS",
        "pays": properties.get("country"),
        "longitude": float(longitude),
        "latitude": float(latitude),
    }

def calcul_itineraire_avec_ferry(lat1, lon1, lat2, lon2, vitesse_kmh, profil, contraintes=None):
    client = _ors_client()
    ors_profile = ORS_PROFILES.get(profil, "driving-car")
    if client is None:
        return None

    candidats = []
    vehicle_options = _ors_vehicle_options(profil, contraintes)
    for ferry in FERRY_ROUTES:
        try:
            depart_summary, depart_geometry, depart_steps = _route_routiere(client, (lat1, lon1), ferry["depart"], ors_profile, vehicle_options)
            arrivee_summary, arrivee_geometry, arrivee_steps = _route_routiere(client, ferry["arrivee"], (lat2, lon2), ors_profile, vehicle_options)
            total = depart_summary["duration"] + ferry["duree_min"] * 60 + arrivee_summary["duration"]
            candidats.append((total, ferry, depart_summary, depart_geometry, depart_steps, arrivee_summary, arrivee_geometry, arrivee_steps))
        except Exception as error:
            logger.info("Liaison ferry indisponible (%s): %s", ferry["nom"], error)

    if not candidats:
        return None

    _, ferry, depart_summary, depart_geometry, depart_steps, arrivee_summary, arrivee_geometry, arrivee_steps = min(candidats, key=lambda item: item[0])
    ferry_distance = distance_km(
        ferry["depart"][0], ferry["depart"][1],
        ferry["arrivee"][0], ferry["arrivee"][1],
    )
    coordinates = depart_geometry["coordinates"] + [ferry["depart"][::-1], ferry["arrivee"][::-1]] + arrivee_geometry["coordinates"]
    return {
        "distance_km": round((depart_summary["distance"] + arrivee_summary["distance"]) / 1000 + ferry_distance, 2),
        "duree_min": round((depart_summary["duration"] + arrivee_summary["duration"]) / 60 + ferry["duree_min"], 1),
        "vitesse_kmh": vitesse_kmh,
        "source": "openrouteservice_ferry",
        "profil_ors": ors_profile,
        "ferry": ferry,
        "steps": depart_steps + [{"instruction": f"Embarquer : {ferry['nom']}", "distance_km": round(ferry_distance, 2), "duree_min": ferry["duree_min"]}] + arrivee_steps,
        "geometry": {"type": "LineString", "coordinates": coordinates},
    }


def _ors_vehicle_options(profil, contraintes):
    if profil not in {"bus", "utilitaire", "camping_car", "poids_lourd"} or not contraintes:
        return None
    restrictions = {}
    mapping = {
        "hauteur_m": "height",
        "largeur_m": "width",
        "longueur_m": "length",
        "poids_max_t": "weight",
    }
    for source_key, ors_key in mapping.items():
        value = contraintes.get(source_key)
        if value is not None:
            restrictions[ors_key] = float(value)
    if not restrictions:
        return None
    return {
        "vehicle_type": "hgv",
        "profile_params": {"restrictions": restrictions},
    }


def calcul_itineraire(
    lat1,
    lon1,
    lat2,
    lon2,
    vitesse_kmh=70,
    profil="voiture",
    contraintes=None,
):
    """
    Retourne un itinéraire adapté au profil, puis utilise les moteurs de secours disponibles.
    Les profils grand véhicule privilégient ORS HGV afin de transmettre le gabarit réel.
    """
    policy = routing_policy(profil)
    heavy_profile = policy["heavy"]
    contraintes = dict(contraintes or {})
    preference = contraintes.pop("route_preference", None) or "recommended"
    avoid_features = [str(x) for x in contraintes.pop("avoid_features", []) if x]
    # Dès qu'une préférence de trajet ou un évitement est demandé, ORS devient
    # l'autorité car il sait appliquer ces contraintes explicitement.
    use_graphhopper_first = (not heavy_profile and preference == "recommended" and not avoid_features)
    if use_graphhopper_first:
        try:
            graphhopper_route = _graphhopper_route(lat1, lon1, lat2, lon2, profil)
            if graphhopper_route is not None:
                graphhopper_route["vitesse_kmh"] = vitesse_kmh
                graphhopper_route["mode_routage"] = policy["preferred"]
                graphhopper_route["profil_demande"] = profil
                return graphhopper_route
        except Exception as error:
            logger.warning("Routage GraphHopper indisponible, fallback ORS: %s", error)

    client = _ors_client()
    ors_profile = ORS_PROFILES.get(profil, "driving-car")

    if client is not None:
        try:
            ors_kwargs = {
                "coordinates": [[lon1, lat1], [lon2, lat2]],
                "profile": ors_profile,
                "format": "geojson",
                "preference": preference if preference in {"recommended", "fastest", "shortest"} else "recommended",
            }
            options = _ors_vehicle_options(profil, contraintes) or {}
            if avoid_features:
                options = dict(options)
                options["avoid_features"] = avoid_features
            if options:
                ors_kwargs["options"] = options
            route = client.directions(**ors_kwargs)
            feature = route["features"][0]
            summary = feature["properties"]["summary"]
            steps = []
            for segment in feature["properties"].get("segments", []):
                for step in segment.get("steps", []):
                    steps.append({
                        "instruction": step.get("instruction", ""),
                        "distance_km": round(step.get("distance", 0) / 1000, 2),
                        "duree_min": round(step.get("duration", 0) / 60, 1),
                    })
            return {
                "distance_km": round(summary["distance"] / 1000, 2),
                "duree_min": round(summary["duration"] / 60, 1),
                "vitesse_kmh": vitesse_kmh,
                "source": "openrouteservice",
                "profil_ors": ors_profile,
                "mode_routage": policy["preferred"],
                "profil_demande": profil,
                "steps": steps,
                "geometry": feature["geometry"],
            }
        except Exception as error:
            logger.warning("Routage ORS indisponible: %s", error)

    if heavy_profile:
        try:
            graphhopper_route = _graphhopper_route(lat1, lon1, lat2, lon2, profil, preference)
            if graphhopper_route is not None:
                graphhopper_route["vitesse_kmh"] = vitesse_kmh
                graphhopper_route["mode_routage"] = "secours_grand_vehicule"
                graphhopper_route["profil_demande"] = profil
                graphhopper_route["avertissement_routage"] = "Secours sans garantie complète des contraintes de gabarit."
                return graphhopper_route
        except Exception as error:
            logger.warning("Routage GraphHopper de secours indisponible: %s", error)

    if policy["allow_driving_fallback"]:
        try:
            fallback = _osrm_route(lat1, lon1, lat2, lon2)
            fallback["vitesse_kmh"] = vitesse_kmh
            fallback["mode_routage"] = "driving_fallback"
            fallback["profil_demande"] = profil
            if profil == "moto":
                fallback["avertissement_routage"] = "Secours automobile : certaines spécificités moto peuvent ne pas être prises en compte."
            elif heavy_profile:
                fallback["avertissement_routage"] = "Secours automobile : les contraintes de gabarit ne sont pas garanties."
            return fallback
        except Exception as error:
            logger.warning("Routage OSRM indisponible, fallback Haversine: %s", error)
    else:
        logger.warning("Secours automobile volontairement ignoré pour le profil %s.", profil)

    dist = distance_km(lat1, lon1, lat2, lon2)
    duree = duree_minutes(dist, vitesse_kmh)
    return {
        "distance_km": round(dist, 2),
        "duree_min": round(duree, 1),
        "vitesse_kmh": vitesse_kmh,
        "source": "haversine_fallback",
        "profil_ors": ors_profile,
        "mode_routage": "estimation_directe",
        "profil_demande": profil,
        "avertissement_routage": "Estimation directe uniquement : aucun moteur de routage adapté n’est disponible.",
        "geometry": {
            "type": "LineString",
            "coordinates": [[lon1, lat1], [lon2, lat2]],
        },
    }
