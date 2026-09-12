from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.alertes import Alerte
from routers.itineraires import VEHICLE_PROFILES

router = APIRouter(prefix="/alertes", tags=["Alertes"])

def _profil_concerne(csv: str | None, profil: str) -> bool:
    valeurs = {v.strip().lower() for v in (csv or "tous").split(",") if v.strip()}
    return "tous" in valeurs or profil.lower() in valeurs

@router.get("/")
def liste_alertes(db: Session = Depends(get_db)):
    return db.query(Alerte).filter(Alerte.actif.is_(True)).all()

@router.get("/profil/{profil}")
def alertes_par_profil(profil: str, db: Session = Depends(get_db)):
    if profil not in VEHICLE_PROFILES:
        raise HTTPException(status_code=404, detail="Profil véhicule inconnu")
    lignes = db.query(Alerte).filter(Alerte.actif.is_(True)).all()
    return {
        "profil": profil,
        "alertes": [a for a in lignes if _profil_concerne(a.profils_csv, profil)],
    }

@router.get("/{alerte_id}")
def element_par_id(alerte_id: int, db: Session = Depends(get_db)):
    element = db.query(Alerte).filter(Alerte.id == alerte_id).first()
    if element is None:
        raise HTTPException(status_code=404, detail="Alerte introuvable")
    return element
