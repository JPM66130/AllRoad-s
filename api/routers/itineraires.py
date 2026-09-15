import json
import math
import uuid
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import func
from sqlalchemy.orm import Session
from db import get_db
from routers.access import require_profile_access
from models.arrets import Arret
from models.compteur import Compteur
from models.itineraires import Itineraire
from models.trajet_details import TrajetDetail
from utils.geo import GeocodingUnavailable, calcul_itineraire, calcul_itineraire_avec_ferry, geocoder, liaisons_ferry, reverse_geocoder
from utils.carburants import get_eu_fuel_prices, get_fuel_prices

router = APIRouter(prefix="/itineraire", tags=["Itinéraires"])

VehicleProfile = Literal[
    "voiture",
    "moto",
    "velo",
    "pieton",
    "bus",
    "utilitaire",
    "camping_car",
    "poids_lourd",
]

MAX_AUTO_TRIPS = 20
MAX_STOPS_PER_TRIP = 20


def _geometry_line_strings(geometry: dict) -> list[list[list[float]]]:
    """Retourne les lignes [lon, lat] d'une géométrie GeoJSON."""
    if not isinstance(geometry, dict):
        return []
    gtype = geometry.get("type")
    if gtype == "Feature":
        return _geometry_line_strings(geometry.get("geometry") or {})
    if gtype == "FeatureCollection":
        lines = []
        for feature in geometry.get("features") or []:
            lines.extend(_geometry_line_strings(feature))
        return lines
    coords = geometry.get("coordinates") or []
    if gtype == "LineString":
        return [coords] if len(coords) >= 2 else []
    if gtype == "MultiLineString":
        return [line for line in coords if isinstance(line, list) and len(line) >= 2]
    if gtype == "GeometryCollection":
        lines = []
        for item in geometry.get("geometries") or []:
            lines.extend(_geometry_line_strings(item))
        return lines
    return []


def _point_segment_distance_m(point_lat: float, point_lon: float, a: list[float], b: list[float]) -> float:
    """Distance locale minimale en mètres entre un point et un segment lon/lat."""
    lat0 = math.radians(point_lat)
    scale_x = 111_320.0 * max(0.01, math.cos(lat0))
    scale_y = 110_540.0
    ax = (float(a[0]) - point_lon) * scale_x
    ay = (float(a[1]) - point_lat) * scale_y
    bx = (float(b[0]) - point_lon) * scale_x
    by = (float(b[1]) - point_lat) * scale_y
    vx, vy = bx - ax, by - ay
    length2 = vx * vx + vy * vy
    if length2 <= 1e-9:
        return math.hypot(ax, ay)
    # Le point de référence est l'origine (0, 0).
    u = max(0.0, min(1.0, -(ax * vx + ay * vy) / length2))
    cx, cy = ax + u * vx, ay + u * vy
    return math.hypot(cx, cy)


def geometry_min_distance_to_point_m(geometry: dict, lat: float, lon: float) -> float | None:
    """Distance minimale point→segments ; None si la géométrie n'est pas exploitable."""
    best = None
    for line in _geometry_line_strings(geometry):
        for a, b in zip(line, line[1:]):
            try:
                distance = _point_segment_distance_m(lat, lon, a, b)
            except (TypeError, ValueError, IndexError):
                continue
            best = distance if best is None else min(best, distance)
    return best


HEAVY_PROFILES = {"bus", "utilitaire", "camping_car", "poids_lourd"}


def routing_assurance(profil: str, result: dict) -> dict:
    """
    Décide si AllRoad's peut autoriser un guidage réel avec le niveau de preuve
    disponible. Pour un grand véhicule, une route automobile de secours reste
    affichable à titre informatif mais ne doit jamais être présentée comme sûre
    pour le gabarit.
    """
    source = str(result.get("source") or "")
    profil_moteur = str(result.get("profil_ors") or "")
    heavy = profil in HEAVY_PROFILES
    hgv_verified = source in {"openrouteservice", "openrouteservice_ferry"} and profil_moteur == "driving-hgv"

    if heavy and not hgv_verified:
        return {
            "guidage_autorise": False,
            "gabarit_verifie_moteur": False,
            "niveau_garantie_routage": "informatif_non_garanti",
            "message_securite_routage": (
                "Itinéraire informatif uniquement : le moteur disponible ne garantit pas "
                "le gabarit de ce véhicule. Le guidage réel reste bloqué jusqu’à un calcul HGV vérifié."
            ),
        }

    return {
        "guidage_autorise": True,
        "gabarit_verifie_moteur": bool(hgv_verified) if heavy else None,
        "niveau_garantie_routage": "hgv_moteur_verifie" if heavy else "profil_standard",
        "message_securite_routage": None,
    }


class ArretCreate(BaseModel):
    nom: str = Field(min_length=1, max_length=80)

    @field_validator("nom")
    @classmethod
    def nettoyer_nom(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Le nom de l’arrêt ne peut pas être vide.")
        return value
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    direction_deg: float = Field(ge=0, lt=360)
    precision_m: float = Field(ge=0, le=100)


class TourneeEndpointUpdate(BaseModel):
    type: Literal["depart", "arrivee"]
    arret_id: int = Field(gt=0)


class TourneeUpdate(BaseModel):
    nom_tournee: str = Field(min_length=1, max_length=80)

    @field_validator("nom_tournee")
    @classmethod
    def nettoyer_nom_tournee(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Le nom de la tournée ne peut pas être vide.")
        return value


VEHICLE_PROFILES = {
    "voiture": {
        "libelle": "Voiture", "vitesse_max_kmh": 130, "hauteur_m": 2.0,
        "largeur_m": 2.0, "longueur_m": 5.0, "poids_max_t": 3.5, "consommation_l_100": 7.0,
    },
    "moto": {
        "libelle": "Moto", "vitesse_max_kmh": 130, "hauteur_m": 1.5,
        "largeur_m": 1.0, "longueur_m": 2.5, "poids_max_t": 0.6, "consommation_l_100": 5.0,
    },
    "velo": {
        "libelle": "Vélo", "vitesse_max_kmh": 45, "hauteur_m": 2.0,
        "largeur_m": 1.0, "longueur_m": 2.2, "poids_max_t": 0.2, "consommation_l_100": 0.0,
    },
    "pieton": {
        "libelle": "Piéton", "vitesse_max_kmh": 8, "hauteur_m": 2.2,
        "largeur_m": 1.0, "longueur_m": 1.0, "poids_max_t": 0.2, "consommation_l_100": 0.0,
    },
    "bus": {
        "libelle": "Bus", "vitesse_max_kmh": 90, "hauteur_m": 4.0,
        "largeur_m": 2.6, "longueur_m": 18.0, "poids_max_t": 19.0, "consommation_l_100": 30.0,
    },
    "utilitaire": {
        "libelle": "Utilitaire", "vitesse_max_kmh": 110, "hauteur_m": 2.8,
        "largeur_m": 2.2, "longueur_m": 7.0, "poids_max_t": 3.5, "consommation_l_100": 10.0,
    },
    "camping_car": {
        "libelle": "Camping-car", "vitesse_max_kmh": 110, "hauteur_m": 3.2,
        "largeur_m": 2.35, "longueur_m": 7.5, "poids_max_t": 3.5, "consommation_l_100": 12.0,
    },
    "poids_lourd": {
        "libelle": "Poids lourd", "vitesse_max_kmh": 90, "hauteur_m": 4.0,
        "largeur_m": 2.55, "longueur_m": 16.5, "poids_max_t": 40.0, "consommation_l_100": 32.0,
    },
}


def _serialize_stop(stop):
    return {
        "id": stop.id,
        "nom": stop.nom,
        "latitude": stop.latitude,
        "longitude": stop.longitude,
        "direction_deg": stop.direction_deg,
        "precision_m": stop.precision_m,
    }


def _serialize_trip(itineraire, db):
    detail = db.query(TrajetDetail).filter(TrajetDetail.itineraire_id == itineraire.id).one_or_none()
    stops = db.query(Arret).filter(Arret.itineraire_id == itineraire.id).order_by(Arret.id).all()
    return {
        "id": itineraire.id,
        "depart": itineraire.depart,
        "arrivee": itineraire.arrivee,
        "lat_depart": itineraire.lat_depart,
        "lon_depart": itineraire.lon_depart,
        "lat_arrivee": itineraire.lat_arrivee,
        "lon_arrivee": itineraire.lon_arrivee,
        "distance_km": itineraire.distance_km,
        "duree_min": itineraire.duree_min,
        "profil": detail.profil if detail else "voiture",
        "nom_tournee": detail.nom_tournee if detail else "Tournée sans nom",
        "sauvegarde_volontaire": bool(detail.sauvegarde_volontaire) if detail else False,
        "statut_diffusion": detail.statut_diffusion if detail else "personnelle",
        "client_id": detail.client_id if detail else None,
        "depot_id": detail.depot_id if detail else None,
        "validee_par": detail.validee_par if detail else None,
        "note_exploitation": detail.note_exploitation if detail else None,
        "geometry": json.loads(detail.geometry_json) if detail else None,
        "arrets": [_serialize_stop(stop) for stop in stops],
    }


def _get_or_create_compteur(db: Session) -> Compteur:
    compteur = db.get(Compteur, 1)
    if compteur is None:
        # Première migration : on initialise le cumul avec l’historique encore disponible.
        total = db.query(func.coalesce(func.sum(Itineraire.distance_km), 0.0)).scalar()
        trajets = db.query(func.count(Itineraire.id)).scalar()
        compteur = Compteur(id=1, total_km=float(total), trajets=int(trajets))
        db.add(compteur)
        db.flush()
    return compteur


@router.get("/profils")
def liste_profils():
    return VEHICLE_PROFILES

@router.get("/ferries")
def liste_ferries():
    return liaisons_ferry()

@router.get("/geocoder")
def rechercher_adresse(
    adresse: str,
    focus_lat: float | None = Query(None, ge=-90, le=90),
    focus_lon: float | None = Query(None, ge=-180, le=180),
):
    try:
        return geocoder(adresse, focus_lat=focus_lat, focus_lon=focus_lon)
    except GeocodingUnavailable as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

@router.get("/carburants")
def prix_carburants():
    return get_fuel_prices()

@router.get("/carburants-europe")
def prix_carburants_europe():
    return get_eu_fuel_prices()

@router.get("/calcul")
def calculer_itineraire(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    vitesse: float = Query(70, gt=0, le=130),
    profil: VehicleProfile = "voiture",
    avec_ferry: bool = False,
    avoid_autoroutes: bool = False,
    avoid_peages: bool = False,
    avoid_ferries: bool = False,
    route_preference: Literal["recommended", "fastest", "shortest"] = "recommended",
    prix_carburant: float = Query(1.85, gt=0, le=10),
    consommation_l_100: float | None = Query(None, ge=0, le=100),
    hauteur_m: float | None = Query(None, gt=0, le=6),
    largeur_m: float | None = Query(None, gt=0, le=4),
    longueur_m: float | None = Query(None, gt=0, le=30),
    poids_max_t: float | None = Query(None, gt=0, le=60),
    vitesse_max_kmh: float | None = Query(None, gt=0, le=130),
    avoid_lat: float | None = Query(None, ge=-90, le=90),
    avoid_lon: float | None = Query(None, ge=-180, le=180),
    avoid_radius_m: float | None = Query(None, ge=10, le=500),
    db: Session = Depends(get_db)
):
    require_profile_access(profil)
    profile_config = dict(VEHICLE_PROFILES[profil])
    for key, value in {
        "hauteur_m": hauteur_m,
        "largeur_m": largeur_m,
        "longueur_m": longueur_m,
        "poids_max_t": poids_max_t,
        "vitesse_max_kmh": vitesse_max_kmh,
    }.items():
        if value is not None:
            profile_config[key] = value
    vitesse_retenue = min(vitesse, profile_config["vitesse_max_kmh"])
    consommation = consommation_l_100 if consommation_l_100 is not None else profile_config["consommation_l_100"]
    taux_peage = {"voiture": 0.09, "moto": 0.06, "velo": 0.0, "pieton": 0.0, "bus": 0.22, "utilitaire": 0.14, "camping_car": 0.14, "poids_lourd": 0.25}[profil]
    route_constraints = dict(profile_config)
    route_constraints["route_preference"] = route_preference
    avoided = []
    if profil not in {"pieton", "velo"} and avoid_autoroutes:
        avoided.append("highways")
    if profil not in {"pieton", "velo"} and avoid_peages:
        avoided.append("tollways")
    if avoid_ferries:
        avoided.append("ferries")
    route_constraints["avoid_features"] = avoided
    ferry_allowed = avec_ferry and not avoid_ferries
    result = calcul_itineraire_avec_ferry(
        lat1, lon1, lat2, lon2, vitesse_retenue, profil, route_constraints
    ) if ferry_allowed else None
    if result is None:
        result = calcul_itineraire(lat1, lon1, lat2, lon2, vitesse_retenue, profil, route_constraints)

    assurance = routing_assurance(profil, result)

    # Garde de sécurité optionnelle, utilisée notamment pour un guidage temporaire
    # vers une zone de retournement. On refuse une route qui repasse au voisinage
    # du blocage au lieu de prétendre qu'elle est sûre.
    avoid_values = (avoid_lat, avoid_lon, avoid_radius_m)
    if any(value is not None for value in avoid_values):
        if not all(value is not None for value in avoid_values):
            raise HTTPException(status_code=422, detail="Les informations de zone à éviter sont incomplètes.")
        min_distance = geometry_min_distance_to_point_m(result.get("geometry") or {}, avoid_lat, avoid_lon)
        if min_distance is None:
            raise HTTPException(
                status_code=409,
                detail="AllRoads ne peut pas vérifier que cet itinéraire évite réellement le blocage. Arrêtez-vous en sécurité et choisissez une autre zone.",
            )
        if min_distance <= avoid_radius_m:
            raise HTTPException(
                status_code=409,
                detail="Cet itinéraire vers la zone proposée passe trop près du blocage. AllRoads ne le propose pas. Arrêtez-vous en sécurité et choisissez une autre zone.",
            )

    itin = Itineraire(
        depart=f"{lat1},{lon1}",
        arrivee=f"{lat2},{lon2}",
        lat_depart=lat1,
        lon_depart=lon1,
        lat_arrivee=lat2,
        lon_arrivee=lon2,
        distance_km=result["distance_km"],
        duree_min=result["duree_min"]
    )

    compteur = _get_or_create_compteur(db)
    db.add(itin)
    db.flush()
    db.add(TrajetDetail(itineraire_id=itin.id, profil=profil, geometry_json=json.dumps(result["geometry"])))
    # SessionLocal utilise autoflush=False : rendre le détail visible avant la purge
    # des trajets automatiques, sinon un 21e trajet peut temporairement échapper à la limite.
    db.flush()
    compteur.total_km += float(result["distance_km"])
    compteur.trajets += 1
    # Les tournées sauvegardées volontairement sont protégées.
    # Seuls les trajets automatiques les plus anciens sont purgés.
    auto_ids = [
        row[0]
        for row in (
            db.query(Itineraire.id)
            .join(TrajetDetail, TrajetDetail.itineraire_id == Itineraire.id)
            .filter(TrajetDetail.sauvegarde_volontaire.is_(False))
            .order_by(Itineraire.id.desc())
            .offset(MAX_AUTO_TRIPS)
            .all()
        )
    ]
    if auto_ids:
        db.query(Arret).filter(Arret.itineraire_id.in_(auto_ids)).delete(synchronize_session=False)
        db.query(TrajetDetail).filter(TrajetDetail.itineraire_id.in_(auto_ids)).delete(synchronize_session=False)
        db.query(Itineraire).filter(Itineraire.id.in_(auto_ids)).delete(synchronize_session=False)
    db.commit()
    db.refresh(itin)

    carburant_eur = round(result["distance_km"] * consommation * prix_carburant / 100, 2)
    peages_eur = 0.0 if avoid_peages else None
    ferry_eur = result.get("ferry", {}).get("prix_eur", 0)
    avertissements_routage = []
    if profil in HEAVY_PROFILES:
        if assurance["guidage_autorise"]:
            avertissements_routage.append(
                "Routage grand véhicule : contraintes transmises au moteur HGV. Vérifiez toujours la signalisation réelle."
            )
        else:
            avertissements_routage.append(assurance["message_securite_routage"])
    if result.get("avertissement_routage"):
        avertissements_routage.append(result["avertissement_routage"])

    return {
        "itineraire_id": itin.id,
        "distance_km": itin.distance_km,
        "duree_min": itin.duree_min,
        "vitesse_kmh": vitesse_retenue,
        "profil": profil,
        "nom_tournee": "Tournée sans nom",
        "contraintes_vehicule": profile_config,
        "avertissements_routage": avertissements_routage,
        "source_routage": result["source"],
        "mode_routage": result.get("mode_routage"),
        "profil_demande": result.get("profil_demande", profil),
        "profil_ors": result["profil_ors"],
        "guidage_autorise": assurance["guidage_autorise"],
        "gabarit_verifie_moteur": assurance["gabarit_verifie_moteur"],
        "niveau_garantie_routage": assurance["niveau_garantie_routage"],
        "message_securite_routage": assurance["message_securite_routage"],
        "ferry": result.get("ferry"),
        "preferences_trajet": {
            "autoroutes_evitees": avoid_autoroutes,
            "peages_evites": avoid_peages,
            "ferries_evites": avoid_ferries,
            "preference": route_preference,
        },
        "etapes": result.get("steps", []),
        "estimation_cout": {
            "carburant_l": round(result["distance_km"] * consommation / 100, 1),
            "prix_carburant_eur_l": prix_carburant,
            "consommation_l_100": consommation,
            "carburant_eur": carburant_eur,
            "peages_eur": peages_eur,
            "ferry_eur": ferry_eur,
            "total_eur": round(carburant_eur + (peages_eur or 0.0) + ferry_eur, 2),
            "precision": "Estimation selon le véhicule actif. Aucun péage n'est inventé à partir du seul fait de rouler sur autoroute ; sans donnée tarifaire réelle, le péage reste à confirmer.",
        },
        "geometry": result["geometry"],
    }


@router.get("/comparaison")
def comparer_itineraires(
    lat1: float, lon1: float, lat2: float, lon2: float,
    vitesse: float = Query(70, gt=0, le=130),
    profil: VehicleProfile = "voiture",
    prix_carburant: float = Query(1.85, gt=0, le=10),
    consommation_l_100: float | None = Query(None, ge=0, le=100),
    hauteur_m: float | None = Query(None, gt=0, le=6),
    largeur_m: float | None = Query(None, gt=0, le=4),
    longueur_m: float | None = Query(None, gt=0, le=30),
    poids_max_t: float | None = Query(None, gt=0, le=60),
    vitesse_max_kmh: float | None = Query(None, gt=0, le=130),
    avoid_autoroutes: bool = False, avoid_peages: bool = False, avoid_ferries: bool = False,
):
    """Compare trois stratégies réelles avec les mêmes préférences conducteur."""
    require_profile_access(profil)
    profile_config = dict(VEHICLE_PROFILES[profil])
    for key, value in {
        "hauteur_m": hauteur_m, "largeur_m": largeur_m, "longueur_m": longueur_m,
        "poids_max_t": poids_max_t, "vitesse_max_kmh": vitesse_max_kmh,
    }.items():
        if value is not None:
            profile_config[key] = value
    vitesse_retenue = min(vitesse, profile_config["vitesse_max_kmh"])
    consommation = consommation_l_100 if consommation_l_100 is not None else profile_config["consommation_l_100"]
    taux_peage = {"voiture": 0.09, "moto": 0.06, "velo": 0.0, "pieton": 0.0, "bus": 0.22, "utilitaire": 0.14, "camping_car": 0.14, "poids_lourd": 0.25}[profil]
    avoided = []
    if avoid_autoroutes: avoided.append("highways")
    if avoid_peages: avoided.append("tollways")
    if avoid_ferries: avoided.append("ferries")
    labels = [("Recommandé", "recommended"), ("Le plus rapide", "fastest"), ("Le plus court", "shortest")]
    candidates = []
    for label, preference in labels:
        constraints = dict(profile_config)
        constraints["route_preference"] = preference
        constraints["avoid_features"] = list(avoided)
        route = calcul_itineraire(lat1, lon1, lat2, lon2, vitesse_retenue, profil, constraints)
        fuel_l = round(route["distance_km"] * consommation / 100, 1)
        fuel_eur = round(fuel_l * prix_carburant, 2)
        toll_eur = 0.0 if avoid_peages else None
        candidates.append({
            "label": label, "preference": preference,
            "distance_km": route["distance_km"], "duree_min": route["duree_min"],
            "consommation_l": fuel_l, "carburant_eur": fuel_eur,
            "peages_eur": toll_eur, "cout_total_eur": round(fuel_eur + (toll_eur or 0.0), 2),
            "source_routage": route.get("source"),
        })
    return {
        "profil": profil,
        "preferences": {"avoid_autoroutes": avoid_autoroutes, "avoid_peages": avoid_peages, "avoid_ferries": avoid_ferries},
        "candidats": candidates,
        "note_cout": "Carburant calculé selon le véhicule actif. Les péages ne sont ajoutés que lorsqu'une donnée tarifaire réelle est disponible ; autoroute ne signifie pas péage.",
    }


@router.get("/compteur")
def compteur_kilometrique(db: Session = Depends(get_db)):
    compteur = _get_or_create_compteur(db)
    db.commit()
    return {
        "total_km": round(float(compteur.total_km), 2),
        "trajets": int(compteur.trajets),
    }


@router.post("/{itineraire_id}/arrets")
def marquer_arret(itineraire_id: int, payload: ArretCreate, db: Session = Depends(get_db)):
    itineraire = db.get(Itineraire, itineraire_id)
    if itineraire is None:
        raise HTTPException(status_code=404, detail="Itinéraire introuvable.")
    detail = db.query(TrajetDetail).filter(TrajetDetail.itineraire_id == itineraire_id).one_or_none()
    if detail is None or detail.profil != "bus":
        raise HTTPException(status_code=422, detail="Les arrêts peuvent uniquement être marqués sur un trajet bus.")
    if db.query(Arret).filter(Arret.itineraire_id == itineraire_id).count() >= MAX_STOPS_PER_TRIP:
        raise HTTPException(status_code=409, detail="Un trajet bus peut contenir au maximum 20 arrêts.")

    arret = Arret(itineraire_id=itineraire_id, **payload.model_dump())
    db.add(arret)
    db.commit()
    db.refresh(arret)
    return _serialize_stop(arret)


@router.put("/{itineraire_id}/tournee/endpoint")
def modifier_extremite_tournee(itineraire_id: int, payload: TourneeEndpointUpdate, db: Session = Depends(get_db)):
    itineraire = db.get(Itineraire, itineraire_id)
    if itineraire is None:
        raise HTTPException(status_code=404, detail="Itineraire introuvable.")
    detail = db.query(TrajetDetail).filter(TrajetDetail.itineraire_id == itineraire_id).one_or_none()
    if detail is None:
        raise HTTPException(status_code=404, detail="Detail de trajet introuvable.")
    if detail.statut_diffusion == "validee":
        raise HTTPException(status_code=409, detail="Une tournee validee ne peut pas etre modifiee directement. Proposez une modification.")
    arret = db.query(Arret).filter(Arret.id == payload.arret_id, Arret.itineraire_id == itineraire_id).one_or_none()
    if arret is None:
        raise HTTPException(status_code=404, detail="Arret introuvable pour cet itineraire.")
    try:
        lieu = reverse_geocoder(arret.latitude, arret.longitude)
    except GeocodingUnavailable:
        lieu = None
    nom = lieu["nom"] if lieu and lieu.get("nom") else arret.nom
    if payload.type == "depart":
        itineraire.depart = nom
        itineraire.lat_depart = arret.latitude
        itineraire.lon_depart = arret.longitude
    else:
        itineraire.arrivee = nom
        itineraire.lat_arrivee = arret.latitude
        itineraire.lon_arrivee = arret.longitude
    db.commit()
    db.refresh(itineraire)
    return {
        "itineraire_id": itineraire_id,
        "arret_id": arret.id,
        "type": payload.type,
        "nom": nom,
        "latitude": arret.latitude,
        "longitude": arret.longitude,
    }

@router.put("/{itineraire_id}/tournee")
def nommer_tournee(itineraire_id: int, payload: TourneeUpdate, db: Session = Depends(get_db)):
    detail = db.query(TrajetDetail).filter(TrajetDetail.itineraire_id == itineraire_id).one_or_none()
    if detail is None:
        raise HTTPException(status_code=404, detail="Itinéraire introuvable.")
    if not detail.tournee_uid:
        detail.tournee_uid = str(uuid.uuid4())
    detail.nom_tournee = payload.nom_tournee
    detail.sauvegarde_volontaire = True
    db.commit()
    return {
        "itineraire_id": itineraire_id,
        "nom_tournee": detail.nom_tournee,
        "sauvegarde_volontaire": True,
    }



@router.delete("/{itineraire_id}/tournee")
def supprimer_tournee_sauvegardee(itineraire_id: int, db: Session = Depends(get_db)):
    """Libère une place parmi les 20 sauvegardes volontaires sans effacer le kilométrage cumulé."""
    detail = db.query(TrajetDetail).filter(TrajetDetail.itineraire_id == itineraire_id).one_or_none()
    if detail is None:
        raise HTTPException(status_code=404, detail="Itinéraire introuvable.")
    if not detail.sauvegarde_volontaire:
        raise HTTPException(status_code=409, detail="Cette tournée n’est pas une sauvegarde volontaire.")

    # On retire la sauvegarde volontaire. Le trajet redevient temporaire et pourra
    # être purgé plus tard avec l'historique automatique. Le compteur reste intact.
    detail.sauvegarde_volontaire = False
    detail.nom_tournee = "Tournée sans nom"
    db.commit()
    return {
        "itineraire_id": itineraire_id,
        "sauvegarde_volontaire": False,
        "message": "Tournée retirée des sauvegardes.",
    }


@router.get("/")
def liste_itineraires(db: Session = Depends(get_db)):
    itineraires = db.query(Itineraire).order_by(Itineraire.id.desc()).all()
    return [_serialize_trip(itineraire, db) for itineraire in itineraires]


