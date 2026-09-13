"""Recherche unifiée des points d'intérêt JEPALYS.

J240 : nom + localité via le géocodeur ORS/Pelias et catégories de proximité
via OpenStreetMap/Overpass. Le routage reste entièrement séparé : un résultat
POI fournit seulement une destination géographique propre.
"""
from __future__ import annotations

import os
from math import asin, cos, radians, sin, sqrt
from time import monotonic
from typing import Any

import httpx
from fastapi import APIRouter, HTTPException, Query

from utils.geo import GeocodingUnavailable, geocoder

router = APIRouter(prefix="/poi", tags=["POI"])
OVERPASS_URL = os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter")
_CACHE: dict[tuple, tuple[float, list[dict[str, Any]]]] = {}
CACHE_SECONDS = 300

CATEGORY_FILTERS = {
    "rest_area": ['["highway"="rest_area"]', '["amenity"="rest_area"]'],
    "parking": ['["amenity"="parking"]'],
    "fuel": ['["amenity"="fuel"]'],
    "mall": ['["shop"="mall"]', '["building"="retail"]', '["landuse"="retail"]'],
    "shop": ['["shop"]'],
    "camping": ['["tourism"="camp_site"]', '["tourism"="caravan_site"]'],
    "motorhome": ['["tourism"="caravan_site"]', '["amenity"="parking"]["motorhome"="yes"]'],
    "water_dump": ['["amenity"="sanitary_dump_station"]', '["amenity"="water_point"]', '["drinking_water"="yes"]'],
    "lpg": ['["amenity"="fuel"]["fuel:lpg"="yes"]'],
}


def _distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0088
    p1, p2 = radians(lat1), radians(lat2)
    dp, dl = radians(lat2-lat1), radians(lon2-lon1)
    a = sin(dp/2)**2 + cos(p1)*cos(p2)*sin(dl/2)**2
    return 2*r*asin(sqrt(a))


def _address(tags: dict[str, Any]) -> str:
    parts = []
    num, street = tags.get("addr:housenumber"), tags.get("addr:street")
    if street:
        parts.append(f"{num} {street}".strip() if num else street)
    for key in ("addr:postcode", "addr:city"):
        if tags.get(key):
            parts.append(str(tags[key]))
    return ", ".join(parts)


def _locality(tags: dict[str, Any]) -> str | None:
    return tags.get("addr:city") or tags.get("addr:place") or tags.get("addr:suburb")


def _kind(tags: dict[str, Any]) -> str:
    if tags.get("highway") == "rest_area" or tags.get("amenity") == "rest_area":
        return "aire"
    if tags.get("amenity") == "parking":
        return "parking"
    if tags.get("amenity") == "fuel" and tags.get("fuel:lpg") == "yes":
        return "gpl"
    if tags.get("amenity") == "fuel":
        return "station"
    if tags.get("shop") == "mall" or tags.get("building") == "retail" or tags.get("landuse") == "retail":
        return "centre_commercial"
    if tags.get("tourism") in {"camp_site", "caravan_site"}:
        return "camping_car" if tags.get("tourism") == "caravan_site" else "camping"
    if tags.get("amenity") in {"sanitary_dump_station", "water_point"} or tags.get("drinking_water") == "yes":
        return "eau_vidange"
    if tags.get("shop"):
        return "commerce"
    return "lieu"


def _overpass_query(lat: float, lon: float, radius_m: int, category: str) -> str:
    filters = CATEGORY_FILTERS.get(category)
    if not filters:
        raise HTTPException(status_code=400, detail="Catégorie POI inconnue.")
    lines = []
    for filt in filters:
        lines.extend([
            f"node(around:{radius_m},{lat},{lon}){filt};",
            f"way(around:{radius_m},{lat},{lon}){filt};",
            f"relation(around:{radius_m},{lat},{lon}){filt};",
        ])
    return "[out:json][timeout:12];\n(\n" + "\n".join(lines) + "\n);\nout center tags;"


async def _nearby(lat: float, lon: float, radius_m: int, category: str) -> list[dict[str, Any]]:
    key = (round(lat, 4), round(lon, 4), radius_m, category)
    now = monotonic()
    cached = _CACHE.get(key)
    if cached and now - cached[0] < CACHE_SECONDS:
        return cached[1]
    headers = {"User-Agent": "JEPALYS-AllRoads/52.9.240 POI", "Accept": "application/json"}
    try:
        async with httpx.AsyncClient(timeout=15.0, headers=headers) as client:
            response = await client.post(OVERPASS_URL, data={"data": _overpass_query(lat, lon, radius_m, category)})
            response.raise_for_status()
            raw = response.json()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Recherche des lieux proches temporairement indisponible.") from exc
    results: list[dict[str, Any]] = []
    seen = set()
    for elem in raw.get("elements", []):
        tags = elem.get("tags") or {}
        center = elem.get("center") or {}
        plat, plon = elem.get("lat", center.get("lat")), elem.get("lon", center.get("lon"))
        if plat is None or plon is None:
            continue
        ident = f"osm-{elem.get('type','x')}-{elem.get('id','0')}"
        if ident in seen:
            continue
        seen.add(ident)
        name = tags.get("name") or tags.get("brand") or {
            "rest_area": "Aire de repos", "parking": "Parking", "fuel": "Station-service",
            "mall": "Centre commercial", "shop": "Commerce", "camping": "Camping",
            "motorhome": "Aire camping-car", "water_dump": "Eau / vidange", "lpg": "Station GPL",
        }.get(category, "Lieu")
        results.append({
            "id": ident,
            "nom": name,
            "type": _kind(tags),
            "latitude": float(plat),
            "longitude": float(plon),
            "adresse": _address(tags),
            "localite": _locality(tags),
            "distance_km": round(_distance_km(lat, lon, float(plat), float(plon)), 2),
            "source": "openstreetmap",
        })
    results.sort(key=lambda x: x["distance_km"])
    results = results[:12]
    _CACHE[key] = (now, results)
    return results


@router.get("/search")
async def search_poi(
    q: str | None = Query(None, min_length=2, max_length=160),
    category: str | None = Query(None),
    lat: float | None = Query(None, ge=-90, le=90),
    lon: float | None = Query(None, ge=-180, le=180),
    radius_m: int = Query(10000, ge=250, le=20000),
):
    """Recherche un lieu par nom/localité ou une catégorie autour du conducteur."""
    if q:
        try:
            places = geocoder(q, focus_lat=lat, focus_lon=lon)
        except GeocodingUnavailable as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        return [
            {
                "id": f"geo-{idx}", "nom": p.get("nom") or q, "type": "lieu",
                "latitude": p["latitude"], "longitude": p["longitude"],
                "adresse": p.get("nom") or q, "localite": None, "source": "ors-pelias",
                "distance_km": round(_distance_km(lat, lon, p["latitude"], p["longitude"]), 2)
                    if lat is not None and lon is not None else None,
            }
            for idx, p in enumerate(places[:8])
        ]
    if category:
        if lat is None or lon is None:
            raise HTTPException(status_code=400, detail="Position nécessaire pour rechercher cette catégorie autour de vous.")
        return await _nearby(lat, lon, radius_m, category)
    raise HTTPException(status_code=400, detail="Indiquez un nom de lieu ou une catégorie.")
