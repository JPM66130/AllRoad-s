from typing import Literal
from time import monotonic
import os

import httpx
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/retournement", tags=["Retournement"])

HeavyProfile = Literal["bus", "utilitaire", "camping_car", "poids_lourd"]


class VehicleSize(BaseModel):
    profil: HeavyProfile
    hauteur_m: float = Field(gt=0, le=6)
    largeur_m: float = Field(gt=0, le=4)
    longueur_m: float = Field(gt=0, le=30)
    poids_t: float = Field(gt=0, le=80)


class TurnaroundCandidate(BaseModel):
    id: str
    nom: str
    type_zone: Literal["rond_point", "parking", "aire", "intersection", "zone_industrielle", "autre"]
    distance_vehicule_m: float = Field(ge=0)
    distance_blocage_m: float = Field(ge=0)
    cote_blocage: Literal["avant", "apres", "retour"]
    accessible: bool = True
    prive: bool = False
    hauteur_max_m: float | None = None
    largeur_min_m: float | None = None
    longueur_utile_m: float | None = None
    poids_max_t: float | None = None
    confiance_source: float = Field(default=0.5, ge=0, le=1)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class TurnaroundSearch(BaseModel):
    vehicule: VehicleSize
    blocage_distance_m: float = Field(gt=0)
    candidats: list[TurnaroundCandidate] = Field(default_factory=list)


def _compatible(vehicle: VehicleSize, c: TurnaroundCandidate) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if not c.accessible:
        reasons.append("zone non accessible")
    if c.prive:
        reasons.append("accès privé")
    # Règle AllRoads : jamais au-delà du blocage.
    if c.cote_blocage == "apres":
        reasons.append("zone située au-delà du blocage")
    if c.cote_blocage == "avant" and c.distance_vehicule_m >= c.distance_blocage_m:
        reasons.append("zone non atteignable avant le blocage")
    if c.hauteur_max_m is not None and vehicle.hauteur_m > c.hauteur_max_m:
        reasons.append("hauteur incompatible")
    if c.largeur_min_m is not None and vehicle.largeur_m > c.largeur_min_m:
        reasons.append("largeur incompatible")
    if c.longueur_utile_m is not None and vehicle.longueur_m > c.longueur_utile_m:
        reasons.append("longueur incompatible")
    if c.poids_max_t is not None and vehicle.poids_t > c.poids_max_t:
        reasons.append("poids incompatible")
    return not reasons, reasons


def _score(c: TurnaroundCandidate) -> float:
    type_bonus = {
        "rond_point": 0.20,
        "aire": 0.16,
        "zone_industrielle": 0.12,
        "parking": 0.10,
        "intersection": 0.06,
        "autre": 0.0,
    }[c.type_zone]
    return round(min(1.0, c.confiance_source * 0.72 + type_bonus + (0.06 if c.cote_blocage == "avant" else 0.02)), 3)


@router.post("/recherche")
def rechercher_zone(payload: TurnaroundSearch):
    compatibles = []
    rejetes = []
    for c in payload.candidats:
        ok, reasons = _compatible(payload.vehicule, c)
        if not ok:
            rejetes.append({"id": c.id, "nom": c.nom, "raisons": reasons})
            continue
        score = _score(c)
        # En bêta, AllRoads refuse d'afficher une zone insuffisamment fiable.
        if score < 0.55:
            rejetes.append({"id": c.id, "nom": c.nom, "raisons": ["niveau de confiance insuffisant"]})
            continue
        compatibles.append({
            "id": c.id,
            "nom": c.nom,
            "type_zone": c.type_zone,
            "distance_vehicule_m": c.distance_vehicule_m,
            "cote_blocage": c.cote_blocage,
            "confiance": score,
            "latitude": c.latitude,
            "longitude": c.longitude,
        })

    compatibles.sort(key=lambda item: (-item["confiance"], item["distance_vehicule_m"]))
    proposition = compatibles[0] if compatibles else None

    if proposition:
        return {
            "trouve": True,
            "proposition": proposition,
            "message": "Zone de retournement proposée. Vérifiez la signalisation et les conditions réelles avant la manœuvre.",
            "action": "Ralentissez et rejoignez uniquement cette zone si son accès reste libre et autorisé.",
            "rejetes": rejetes,
        }

    return {
        "trouve": False,
        "proposition": None,
        "message": "Aucune zone de retournement suffisamment fiable et compatible n’a été identifiée.",
        "action": "Ne tentez pas de demi-tour improvisé. Arrêtez-vous uniquement dans un endroit autorisé et sûr si nécessaire.",
        "rejetes": rejetes,
    }


class MapFeature(BaseModel):
    id: str
    nom: str = "Zone sans nom"
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    type_zone: Literal["rond_point", "parking", "aire", "intersection", "zone_industrielle", "autre"]
    prive: bool = False
    accessible: bool = True
    hauteur_max_m: float | None = None
    largeur_min_m: float | None = None
    longueur_utile_m: float | None = None
    poids_max_t: float | None = None
    confiance_source: float = Field(default=0.5, ge=0, le=1)


class MapDiscoveryRequest(BaseModel):
    vehicule: VehicleSize
    vehicule_lat: float = Field(ge=-90, le=90)
    vehicule_lon: float = Field(ge=-180, le=180)
    blocage_lat: float = Field(ge=-90, le=90)
    blocage_lon: float = Field(ge=-180, le=180)
    blocage_distance_m: float = Field(gt=0)
    zones: list[MapFeature] = Field(default_factory=list)


def _distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    from math import asin, cos, radians, sin, sqrt
    r = 6371000.0
    p1, p2 = radians(lat1), radians(lat2)
    dp, dl = radians(lat2-lat1), radians(lon2-lon1)
    a = sin(dp/2)**2 + cos(p1)*cos(p2)*sin(dl/2)**2
    return 2*r*asin(sqrt(a))


@router.post("/decouverte-carte")
def decouvrir_zones(payload: MapDiscoveryRequest):
    """Transforme des objets cartographiques proches en candidats sûrs.

    Cette étape ne télécharge aucune carte : elle analyse les objets fournis par
    la couche cartographique. Une zone plus proche du blocage que le véhicule
    est considérée "avant" seulement si elle reste atteignable avant l'obstacle.
    Les objets au-delà du blocage sont explicitement marqués puis rejetés par
    le filtre V27.
    """
    candidats = []
    for zone in payload.zones:
        dv = _distance_m(payload.vehicule_lat, payload.vehicule_lon, zone.latitude, zone.longitude)
        db = _distance_m(payload.blocage_lat, payload.blocage_lon, zone.latitude, zone.longitude)

        # Heuristique prudente : si rejoindre la zone depuis le véhicule demande
        # de dépasser la distance connue jusqu'au blocage, elle est "après".
        # Les zones situées derrière/proches du véhicule restent "retour".
        if dv >= payload.blocage_distance_m:
            side = "apres"
        else:
            distance_vehicle_to_block = _distance_m(
                payload.vehicule_lat, payload.vehicule_lon,
                payload.blocage_lat, payload.blocage_lon
            )
            # Une zone qui s'éloigne nettement du blocage est une solution de retour.
            side = "retour" if db > distance_vehicle_to_block + 30 else "avant"

        candidats.append(TurnaroundCandidate(
            id=zone.id, nom=zone.nom, type_zone=zone.type_zone,
            distance_vehicule_m=round(dv, 1),
            distance_blocage_m=payload.blocage_distance_m,
            cote_blocage=side, accessible=zone.accessible, prive=zone.prive,
            hauteur_max_m=zone.hauteur_max_m, largeur_min_m=zone.largeur_min_m,
            longueur_utile_m=zone.longueur_utile_m, poids_max_t=zone.poids_max_t,
            confiance_source=zone.confiance_source,
            latitude=zone.latitude, longitude=zone.longitude,
        ))

    result = rechercher_zone(TurnaroundSearch(
        vehicule=payload.vehicule,
        blocage_distance_m=payload.blocage_distance_m,
        candidats=candidats,
    ))
    result["zones_analysees"] = len(payload.zones)
    result["source"] = "objets_cartographiques"
    return result


OVERPASS_URL = os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter")
_OVERPASS_CACHE: dict[tuple[float, float, int], tuple[float, list[dict]]] = {}
OVERPASS_CACHE_SECONDS = 300


def _overpass_query(lat: float, lon: float, radius_m: int) -> str:
    # Recherche volontairement limitée aux objets utiles à un retournement.
    return f"""[out:json][timeout:12];
(
  node(around:{radius_m},{lat},{lon})["junction"="roundabout"];
  way(around:{radius_m},{lat},{lon})["junction"="roundabout"];
  node(around:{radius_m},{lat},{lon})["amenity"="parking"];
  way(around:{radius_m},{lat},{lon})["amenity"="parking"];
  node(around:{radius_m},{lat},{lon})["highway"="rest_area"];
  way(around:{radius_m},{lat},{lon})["highway"="rest_area"];
  node(around:{radius_m},{lat},{lon})["landuse"="industrial"];
  way(around:{radius_m},{lat},{lon})["landuse"="industrial"];
);
out center tags;"""


def _feature_type(tags: dict) -> str:
    if tags.get("junction") == "roundabout":
        return "rond_point"
    if tags.get("amenity") == "parking":
        return "parking"
    if tags.get("highway") == "rest_area":
        return "aire"
    if tags.get("landuse") == "industrial":
        return "zone_industrielle"
    return "autre"


def _to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _osm_to_zone(element: dict) -> dict | None:
    tags = element.get("tags") or {}
    center = element.get("center") or {}
    lat = element.get("lat", center.get("lat"))
    lon = element.get("lon", center.get("lon"))
    if lat is None or lon is None:
        return None

    access = tags.get("access")
    private = access in {"private", "customers", "permit"}

    # OSM n'a pas toujours ces dimensions. Absence = inconnue, jamais "validée".
    maxheight = _to_float(tags.get("maxheight"))
    maxweight = _to_float(tags.get("maxweight"))
    maxlength = _to_float(tags.get("maxlength"))
    maxwidth = _to_float(tags.get("maxwidth"))

    # Source OSM seule = confiance volontairement modérée.
    # Les dimensions explicites augmentent légèrement la confiance.
    confidence = 0.56
    if _feature_type(tags) == "rond_point":
        confidence = 0.68
    elif _feature_type(tags) in {"aire", "parking"}:
        confidence = 0.62
    if any(v is not None for v in (maxheight, maxweight, maxlength, maxwidth)):
        confidence = min(0.82, confidence + 0.08)

    return {
        "id": f"osm-{element.get('type','x')}-{element.get('id','0')}",
        "nom": tags.get("name") or {
            "rond_point": "Rond-point",
            "parking": "Parking",
            "aire": "Aire",
            "zone_industrielle": "Zone industrielle",
            "autre": "Zone cartographique",
        }[_feature_type(tags)],
        "latitude": float(lat),
        "longitude": float(lon),
        "type_zone": _feature_type(tags),
        "prive": private,
        "accessible": access not in {"no", "private"},
        "hauteur_max_m": maxheight,
        "largeur_min_m": maxwidth,
        "longueur_utile_m": maxlength,
        "poids_max_t": maxweight,
        "confiance_source": confidence,
    }


async def _fetch_overpass_zones(lat: float, lon: float, radius_m: int) -> list[dict]:
    key = (round(lat, 4), round(lon, 4), int(radius_m))
    cached = _OVERPASS_CACHE.get(key)
    now = monotonic()
    if cached and now - cached[0] < OVERPASS_CACHE_SECONDS:
        return cached[1]

    headers = {
        "User-Agent": "AllRoads-beta/0.1 turnaround-discovery",
        "Accept": "application/json",
    }
    async with httpx.AsyncClient(timeout=15.0, headers=headers) as client:
        response = await client.post(OVERPASS_URL, data={"data": _overpass_query(lat, lon, radius_m)})
        response.raise_for_status()
        raw = response.json()

    zones = []
    seen = set()
    for element in raw.get("elements", []):
        zone = _osm_to_zone(element)
        if not zone or zone["id"] in seen:
            continue
        seen.add(zone["id"])
        zones.append(zone)

    _OVERPASS_CACHE[key] = (now, zones)
    return zones


class LiveMapDiscoveryRequest(BaseModel):
    vehicule: VehicleSize
    vehicule_lat: float = Field(ge=-90, le=90)
    vehicule_lon: float = Field(ge=-180, le=180)
    blocage_lat: float = Field(ge=-90, le=90)
    blocage_lon: float = Field(ge=-180, le=180)
    blocage_distance_m: float = Field(gt=0)
    rayon_m: int = Field(default=1200, ge=200, le=2500)


@router.post("/decouverte-live")
async def decouverte_live(payload: LiveMapDiscoveryRequest):
    try:
        zones = await _fetch_overpass_zones(payload.vehicule_lat, payload.vehicule_lon, payload.rayon_m)
    except (httpx.HTTPError, ValueError):
        return {
            "trouve": False,
            "proposition": None,
            "message": "La carte détaillée n’est pas disponible pour le moment.",
            "action": "Ne tentez pas de demi-tour improvisé. Utilisez uniquement un endroit clairement autorisé et adapté.",
            "zones_analysees": 0,
            "source": "indisponible",
        }

    discovery = MapDiscoveryRequest(
        vehicule=payload.vehicule,
        vehicule_lat=payload.vehicule_lat,
        vehicule_lon=payload.vehicule_lon,
        blocage_lat=payload.blocage_lat,
        blocage_lon=payload.blocage_lon,
        blocage_distance_m=payload.blocage_distance_m,
        zones=[MapFeature(**z) for z in zones],
    )
    result = decouvrir_zones(discovery)
    result["source"] = "OpenStreetMap"
    result["rayon_m"] = payload.rayon_m
    return result
