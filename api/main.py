"""Application bêta AllRoads."""

from collections import defaultdict, deque
from pathlib import Path
from ipaddress import ip_address
from typing import Any
from datetime import datetime, timedelta
import hashlib
import hmac
import os
import sys
import time
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict


# Les modules historiques utilisent des imports tels que ``from db import ...``.
# Garder ce dossier dans le chemin rend l'application utilisable depuis la
# racine du dépôt (Render) comme depuis le dossier api (Docker).
API_DIR = Path(__file__).resolve().parent
if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

from db import Base, SessionLocal, engine  # noqa: E402
from sqlalchemy import inspect, text  # noqa: E402
from models import (  # noqa: F401, E402
    alertes as alertes_model,
    arrets,
    compteur as compteur_model,
    itineraires,
    parkings as parkings_model,
    pays as pays_model,
    peages as peages_model,
    restrictions as restrictions_model,
    spots as spots_model,
    stations as stations_model,
    trajet_details,
    usage_stats as usage_stats_model,
)
from routers import access, alertes, itineraires as itineraires_router, parkings, pays, peages, restrictions, spots, stations, turnaround  # noqa: E402
from branding import BRANDABLE_PROFILES, DEFAULT_BRANDING  # noqa: E402


def _cors_origins():
    configured = os.getenv("CORS_ORIGINS", "").strip()
    if configured:
        return [origin.strip() for origin in configured.split(",") if origin.strip()]
    return ["http://127.0.0.1:8000", "http://localhost:8000"]


APP_VERSION = "V52.9.102"
BUILD_VERSION = "J237"
app = FastAPI(title="AllRoads API", description="API AllRoads", version=APP_VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_ACCESS_TOKEN = os.getenv("API_ACCESS_TOKEN")
TESTER_ACCESS_TOKEN = os.getenv("TESTER_ACCESS_TOKEN", "")
OWNER_ACCESS_TOKEN = os.getenv("OWNER_ACCESS_TOKEN", "")
ACCESS_COOKIE = "allroads_access_token"
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "20"))
request_times = defaultdict(deque)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()

if ENVIRONMENT == "production" and not API_ACCESS_TOKEN:
    raise RuntimeError("API_ACCESS_TOKEN est requis lorsque ENVIRONMENT=production.")


def _is_local(request: Request) -> bool:
    host = request.client.host if request.client else ""
    if host in {"localhost", "testclient"}:
        return True
    try:
        adresse = ip_address(host)
    except ValueError:
        return False
    # Le WP35 et le PC communiquent sur le LAN privé : ils ne doivent pas être
    # bloqués par la limitation destinée aux clients Internet.
    return adresse.is_loopback or adresse.is_private


def _role_for_token(token: str) -> str | None:
    clean = (token or "").strip()
    if not clean:
        return None
    if OWNER_ACCESS_TOKEN and hmac.compare_digest(clean, OWNER_ACCESS_TOKEN):
        return "owner"
    if TESTER_ACCESS_TOKEN and hmac.compare_digest(clean, TESTER_ACCESS_TOKEN):
        return "tester"
    if API_ACCESS_TOKEN and hmac.compare_digest(clean, API_ACCESS_TOKEN):
        return "owner"
    return None


def _request_access_role(request: Request) -> str | None:
    if _is_local(request):
        return "owner"
    bearer = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
    cookie = request.cookies.get(ACCESS_COOKIE, "")
    return _role_for_token(bearer) or _role_for_token(cookie)


@app.middleware("http")
async def protect_and_rate_limit(request: Request, call_next):
    role = _request_access_role(request)
    role_token = access.CURRENT_ACCESS_ROLE.set(role or "tester")
    try:
        public_path = request.url.path in {"/", "/health", "/docs", "/openapi.json", "/version", "/branding"}
        entry_path = request.url.path.startswith("/essais-route/") or request.url.path.startswith("/acces-interne/")
        if public_path or entry_path or request.url.path.startswith("/app"):
            response = await call_next(request)
            if request.url.path.startswith("/app"):
                response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
                response.headers["Pragma"] = "no-cache"
                response.headers["Expires"] = "0"
            return response

        if ENVIRONMENT != "production" and request.url.path.startswith("/test-bridge"):
            return await call_next(request)

        remote_host = request.client.host if request.client else "unknown"
        if not _is_local(request):
            if role is None and any((API_ACCESS_TOKEN, TESTER_ACCESS_TOKEN, OWNER_ACCESS_TOKEN)):
                return JSONResponse(status_code=401, content={"detail": "Accès Essais route requis."})

            now = time.monotonic()
            history = request_times[remote_host]
            while history and now - history[0] >= 60:
                history.popleft()
            if len(history) >= RATE_LIMIT_PER_MINUTE:
                return JSONResponse(status_code=429, content={"detail": "Trop de requêtes. Réessayez dans une minute."})
            history.append(now)

        return await call_next(request)
    finally:
        access.CURRENT_ACCESS_ROLE.reset(role_token)


# La création est idempotente. La faire au chargement évite une première
# requête en erreur dans les outils qui ne déclenchent pas les événements de
# démarrage (certains clients de test, notamment).
Base.metadata.create_all(bind=engine)

# Migration légère pour les installations existantes : create_all ne rajoute
# pas une colonne à une table SQLite déjà créée.
if "trajet_details" in inspect(engine).get_table_names():
    colonnes = {col["name"] for col in inspect(engine).get_columns("trajet_details")}
    if "sauvegarde_volontaire" not in colonnes:
        with engine.begin() as connexion:
            connexion.execute(
                text("ALTER TABLE trajet_details ADD COLUMN sauvegarde_volontaire BOOLEAN NOT NULL DEFAULT 0")
            )


def _ajouter_colonnes_sqlite(table: str, definitions: dict[str, str]):
    if table not in inspect(engine).get_table_names():
        return
    existantes = {col["name"] for col in inspect(engine).get_columns(table)}
    with engine.begin() as connexion:
        for nom, definition in definitions.items():
            if nom not in existantes:
                connexion.execute(text(f"ALTER TABLE {table} ADD COLUMN {nom} {definition}"))

_ajouter_colonnes_sqlite("restrictions", {
    "profils_csv": "VARCHAR NOT NULL DEFAULT 'tous'",
    "hauteur_limite_m": "FLOAT",
    "largeur_limite_m": "FLOAT",
    "longueur_limite_m": "FLOAT",
    "poids_limite_t": "FLOAT",
    "niveau": "VARCHAR NOT NULL DEFAULT 'info'",
    "actif": "BOOLEAN NOT NULL DEFAULT 1",
})
_ajouter_colonnes_sqlite("alertes", {
    "profils_csv": "VARCHAR NOT NULL DEFAULT 'tous'",
    "niveau": "VARCHAR NOT NULL DEFAULT 'info'",
    "latitude": "FLOAT",
    "longitude": "FLOAT",
    "source": "VARCHAR",
    "actif": "BOOLEAN NOT NULL DEFAULT 1",
})


@app.get("/", tags=["Santé"])
def root():
    return {"status": "ok", "message": "AllRoads bêta opérationnelle"}


@app.get("/health", tags=["Santé"])
def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# V52.4 — Pont local de test PC ↔ téléphone
# ---------------------------------------------------------------------------
# Ce pont n'est jamais un mécanisme de production. Il conserve seulement en
# mémoire l'état du téléphone et la dernière commande demandée depuis la
# console PC. Un redémarrage du serveur remet tout à zéro.
_TEST_BRIDGE = {
    "last_seen": 0.0,
    "phone": {},
    "command_id": 0,
    "command": None,
    "command_payload": {},
}


class TestBridgeSync(BaseModel):
    last_command_id: int = 0
    phone: dict[str, Any] = {}


class TestBridgeCommand(BaseModel):
    command: str
    payload: dict[str, Any] = {}


def _require_local_test_bridge(request: Request) -> None:
    if ENVIRONMENT == "production":
        raise HTTPException(status_code=404, detail="Outil de test indisponible.")
    host = request.client.host if request.client else ""
    try:
        address = ip_address(host)
        allowed = address.is_private or address.is_loopback or address.is_link_local
    except ValueError:
        allowed = host in {"localhost"}
    if not allowed:
        raise HTTPException(status_code=403, detail="Outil réservé au réseau local.")


@app.post("/test-bridge/sync", tags=["Développement"])
async def test_bridge_sync(data: TestBridgeSync, request: Request):
    _require_local_test_bridge(request)
    _TEST_BRIDGE["last_seen"] = time.time()
    _TEST_BRIDGE["phone"] = dict(data.phone or {})
    if int(data.last_command_id or 0) < _TEST_BRIDGE["command_id"]:
        return {
            "connected": True,
            "command_id": _TEST_BRIDGE["command_id"],
            "command": _TEST_BRIDGE["command"],
            "payload": _TEST_BRIDGE["command_payload"],
        }
    return {"connected": True, "command_id": _TEST_BRIDGE["command_id"], "command": None, "payload": {}}


@app.get("/test-console", include_in_schema=False)
async def test_console(request: Request):
    _require_local_test_bridge(request)
    console_file = API_DIR / "frontend" / "test-console.html"
    if not console_file.is_file():
        raise HTTPException(status_code=404, detail="Console de test indisponible.")
    return FileResponse(str(console_file), media_type="text/html")


@app.get("/test-bridge/status", tags=["Développement"])
async def test_bridge_status(request: Request):
    _require_local_test_bridge(request)
    age = max(0.0, time.time() - float(_TEST_BRIDGE["last_seen"] or 0.0))
    return {
        "connected": bool(_TEST_BRIDGE["last_seen"] and age < 6.0),
        "seconds_since_phone": round(age, 1) if _TEST_BRIDGE["last_seen"] else None,
        "phone": _TEST_BRIDGE["phone"],
        "command_id": _TEST_BRIDGE["command_id"],
    }


@app.post("/test-bridge/command", tags=["Développement"])
async def test_bridge_command(data: TestBridgeCommand, request: Request):
    _require_local_test_bridge(request)
    allowed = {"home", "back", "profile", "demo", "start", "incident", "prepare", "vehicles"}
    if data.command not in allowed:
        raise HTTPException(status_code=400, detail="Commande de test inconnue.")
    _TEST_BRIDGE["command_id"] += 1
    _TEST_BRIDGE["command"] = data.command
    _TEST_BRIDGE["command_payload"] = dict(data.payload or {})
    return {"ok": True, "command_id": _TEST_BRIDGE["command_id"]}


# ---------------------------------------------------------------------------
# V52.8.8 — Compteur statistique d’utilisation « aveugle »
# ---------------------------------------------------------------------------
# Principe de minimisation : ce compteur ne reçoit ni ne stocke coordonnées,
# départ, destination, historique de trajet, adresse IP ni user-agent.
# Une session ne devient significative qu’après 30 s d’utilisation active.
USAGE_QUALIFIED_SECONDS = 30.0
USAGE_HEARTBEAT_CAP_SECONDS = 45.0
USAGE_ALLOWED_PROFILES = {
    "pieton", "velo", "moto", "voiture", "utilitaire",
    "camping_car", "bus", "poids_lourd"
}
USAGE_ALLOWED_MODES = {"navigation", "simulation"}
USAGE_STATS_SALT = os.getenv("USAGE_STATS_SALT", "allroads-development-only")


class UsageStart(BaseModel):
    installation_token: str
    profile: str
    mode: str = "navigation"

    model_config = ConfigDict(extra="forbid")


class UsagePing(BaseModel):
    session_id: str

    model_config = ConfigDict(extra="forbid")


def _usage_user_hash(token: str) -> str:
    clean = (token or "").strip()[:160]
    if len(clean) < 12:
        raise HTTPException(status_code=400, detail="Identifiant statistique invalide.")
    return hashlib.sha256(f"{USAGE_STATS_SALT}:{clean}".encode("utf-8")).hexdigest()


def _usage_validate_profile(profile: str) -> str:
    value = (profile or "").strip().lower()
    if value not in USAGE_ALLOWED_PROFILES:
        raise HTTPException(status_code=400, detail="Profil statistique inconnu.")
    return value


def _usage_validate_mode(mode: str) -> str:
    value = (mode or "navigation").strip().lower()
    if value not in USAGE_ALLOWED_MODES:
        raise HTTPException(status_code=400, detail="Mode statistique inconnu.")
    return value


def _usage_credit(session, now: datetime) -> None:
    delta = max(0.0, (now - session.last_seen_at).total_seconds())
    # Un onglet abandonné ou un téléphone verrouillé ne doit pas gonfler le compteur.
    session.active_seconds = float(session.active_seconds or 0.0) + min(delta, USAGE_HEARTBEAT_CAP_SECONDS)
    session.last_seen_at = now
    session.qualified = session.active_seconds >= USAGE_QUALIFIED_SECONDS


@app.post("/usage/session/start", tags=["Statistiques d’utilisation"])
def usage_session_start(data: UsageStart):
    now = datetime.utcnow()
    session = usage_stats_model.UsageSession(
        id=str(uuid.uuid4()),
        user_hash=_usage_user_hash(data.installation_token),
        profile=_usage_validate_profile(data.profile),
        mode=_usage_validate_mode(data.mode),
        started_at=now,
        last_seen_at=now,
        active_seconds=0.0,
        qualified=False,
    )
    db = SessionLocal()
    try:
        db.add(session)
        db.commit()
        return {"session_id": session.id, "qualified_after_seconds": int(USAGE_QUALIFIED_SECONDS)}
    finally:
        db.close()


@app.post("/usage/session/heartbeat", tags=["Statistiques d’utilisation"])
def usage_session_heartbeat(data: UsagePing):
    db = SessionLocal()
    try:
        session = db.query(usage_stats_model.UsageSession).filter_by(id=data.session_id).first()
        # Un ancien client PWA peut émettre un dernier heartbeat juste après un
        # redémarrage du serveur. Ce cas est attendu et ne doit pas polluer le
        # banc d'essai avec un faux voyant rouge HTTP 404.
        if not session or session.ended_at is not None:
            return {"ok": False, "stale": True, "qualified": False}
        _usage_credit(session, datetime.utcnow())
        db.commit()
        return {"ok": True, "stale": False, "qualified": bool(session.qualified)}
    finally:
        db.close()


@app.post("/usage/session/end", tags=["Statistiques d’utilisation"])
def usage_session_end(data: UsagePing):
    db = SessionLocal()
    try:
        session = db.query(usage_stats_model.UsageSession).filter_by(id=data.session_id).first()
        if not session:
            return {"ok": True}
        if session.ended_at is None:
            now = datetime.utcnow()
            _usage_credit(session, now)
            session.ended_at = now
            db.commit()
        return {"ok": True, "qualified": bool(session.qualified), "active_seconds": round(float(session.active_seconds or 0.0), 1)}
    finally:
        db.close()


@app.get("/usage/stats", tags=["Statistiques d’utilisation"])
def usage_stats(period: str = "month"):
    period = (period or "month").lower()
    now = datetime.utcnow()
    if period == "day":
        since = now - timedelta(days=1)
    elif period == "week":
        since = now - timedelta(days=7)
    elif period == "month":
        since = now - timedelta(days=30)
    else:
        raise HTTPException(status_code=400, detail="Période attendue : day, week ou month.")

    db = SessionLocal()
    try:
        sessions = (db.query(usage_stats_model.UsageSession)
                    .filter(usage_stats_model.UsageSession.started_at >= since)
                    .filter(usage_stats_model.UsageSession.qualified.is_(True))
                    .all())
        users = {s.user_hash for s in sessions}
        total_seconds = sum(float(s.active_seconds or 0.0) for s in sessions)
        per_profile = {}
        for name in sorted(USAGE_ALLOWED_PROFILES):
            selected = [s for s in sessions if s.profile == name]
            seconds = sum(float(s.active_seconds or 0.0) for s in selected)
            per_profile[name] = {
                "active_users": len({s.user_hash for s in selected}),
                "sessions": len(selected),
                "total_seconds": round(seconds, 1),
                "total_hours": round(seconds / 3600.0, 2),
            }
        return {
            "period": period,
            "active_users": len(users),
            "sessions": len(sessions),
            "total_seconds": round(total_seconds, 1),
            "total_hours": round(total_seconds / 3600.0, 2),
            "average_seconds_per_active_user": round(total_seconds / len(users), 1) if users else 0.0,
            "profiles": per_profile,
            "bus_vs_voiture": {"bus": per_profile["bus"], "voiture": per_profile["voiture"]},
            "privacy": {
                "stores_geography": False,
                "stores_origin_destination": False,
                "stores_ip_or_user_agent": False,
                "identifier": "server-side salted hash of a random installation token",
                "qualified_session_seconds": int(USAGE_QUALIFIED_SECONDS),
            },
        }
    finally:
        db.close()


@app.get("/version")
def version_allroads():
    return {"application": "AllRoads", "version": APP_VERSION}


@app.get("/branding")
def branding_allroads():
    """Contrat public de branding. V52.9.31 : branding désactivé par défaut."""
    return {**DEFAULT_BRANDING.public_dict(), "supported_profiles": list(BRANDABLE_PROFILES)}


def _entry_page(title: str, subtitle: str, target: str) -> str:
    return f"""<!doctype html><html lang='fr'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{title}</title><style>body{{margin:0;background:#f5f8fb;font-family:system-ui,sans-serif;color:#0b2e63;display:grid;min-height:100vh;place-items:center}}main{{width:min(92vw,520px);text-align:center}}img{{width:100%;border-radius:28px;box-shadow:0 12px 34px #0002}}p{{font-weight:700}}a{{display:inline-block;margin-top:12px;padding:15px 28px;border-radius:999px;background:#087fea;color:#fff;text-decoration:none;font-weight:900;font-size:20px}}</style></head><body><main><img src='/app/assets/essais-route.png' alt='Essais route'><p>{subtitle}</p><a href='{target}'>Ouvrir</a></main></body></html>"""


@app.get("/essais-route/{token}", response_class=HTMLResponse)
def essais_route_entry(token: str):
    if not TESTER_ACCESS_TOKEN or not hmac.compare_digest(token, TESTER_ACCESS_TOKEN):
        raise HTTPException(status_code=404, detail="Lien indisponible")
    response = HTMLResponse(_entry_page("Essais route", "Accès chauffeur testeur", "/app/?entry=essais-route"))
    response.set_cookie(ACCESS_COOKIE, token, httponly=True, secure=ENVIRONMENT == "production", samesite="lax", max_age=60*60*24*90)
    return response


@app.get("/acces-interne/{token}", response_class=HTMLResponse)
def owner_entry(token: str):
    if not OWNER_ACCESS_TOKEN or not hmac.compare_digest(token, OWNER_ACCESS_TOKEN):
        raise HTTPException(status_code=404, detail="Lien indisponible")
    response = HTMLResponse(_entry_page("Accès interne", "Accès personnel complet", "/app/?entry=interne"))
    response.set_cookie(ACCESS_COOKIE, token, httponly=True, secure=ENVIRONMENT == "production", samesite="lax", max_age=60*60*24*180)
    return response


app.include_router(access.router)
app.include_router(itineraires_router.router)
app.include_router(pays.router)
app.include_router(stations.router)
app.include_router(spots.router)
app.include_router(parkings.router)
app.include_router(alertes.router)
app.include_router(peages.router)
app.include_router(restrictions.router)
app.include_router(turnaround.router)

FRONTEND_DIR = API_DIR / "frontend"
if FRONTEND_DIR.is_dir():
    app.mount("/app", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="app")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
