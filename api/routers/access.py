from contextvars import ContextVar
from datetime import datetime, timezone
import os
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/access", tags=["access"])

ALL_PROFILES = ("pieton", "velo", "moto", "voiture", "utilitaire", "camping_car", "bus", "poids_lourd")
DEFAULT_LAUNCH_PROFILES = ("voiture", "bus")
VALID_STATES = {"TEST", "ACTIF", "EXPIRE", "SUSPENDU", "PRO"}
CURRENT_ACCESS_ROLE = ContextVar("allroads_access_role", default="tester")


def _state():
    return os.getenv("ALLROADS_ACCESS_STATE", "TEST").strip().upper()


def _trial_end():
    raw = os.getenv("ALLROADS_TRIAL_END", "").strip()
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        return None


def access_snapshot(role: str | None = None):
    role = (role or CURRENT_ACCESS_ROLE.get() or "tester").strip().lower()
    if role == "owner":
        return {
            "role": "owner",
            "state": "PRO",
            "service_enabled": True,
            "unlocked_profiles": list(ALL_PROFILES),
            "visible_profiles": list(ALL_PROFILES),
            "trial_end": None,
        }

    state = _state()
    if state not in VALID_STATES:
        state = "TEST"

    trial_end = _trial_end()
    now = datetime.now(timezone.utc)
    effective_state = state
    if state == "TEST" and trial_end is not None and now >= trial_end:
        effective_state = "EXPIRE"

    if effective_state in {"ACTIF", "PRO"}:
        unlocked = list(ALL_PROFILES)
        service_enabled = True
    elif effective_state == "TEST":
        unlocked = list(DEFAULT_LAUNCH_PROFILES)
        service_enabled = True
    else:
        unlocked = []
        service_enabled = False

    return {
        "role": "tester",
        "state": effective_state,
        "service_enabled": service_enabled,
        "unlocked_profiles": unlocked,
        "visible_profiles": list(ALL_PROFILES),
        "trial_end": trial_end.isoformat() if trial_end else None,
    }


def require_profile_access(profile: str):
    access = access_snapshot()
    if not access["service_enabled"]:
        raise HTTPException(status_code=403, detail={
            "code": "SERVICE_LOCKED",
            "state": access["state"],
            "message": "La période d’accès AllRoads est terminée ou suspendue.",
        })
    if profile not in access["unlocked_profiles"]:
        raise HTTPException(status_code=403, detail={
            "code": "PROFILE_LOCKED",
            "profile": profile,
            "message": "Ce profil est visible mais n’est pas encore déverrouillé pour cet accès.",
        })
    return access


@router.get("")
def get_access():
    return access_snapshot()
