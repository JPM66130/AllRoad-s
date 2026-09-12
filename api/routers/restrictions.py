from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db import get_db
from models.restrictions import Restriction
from routers.itineraires import VEHICLE_PROFILES

router = APIRouter(prefix="/restrictions", tags=["Restrictions"])

def _profil_concerne(csv: str | None, profil: str) -> bool:
    valeurs = {v.strip().lower() for v in (csv or "tous").split(",") if v.strip()}
    return "tous" in valeurs or profil.lower() in valeurs

def _declenchee(r: Restriction, vehicule: dict) -> bool:
    limites = [
        (r.hauteur_limite_m, vehicule["hauteur_m"]),
        (r.largeur_limite_m, vehicule["largeur_m"]),
        (r.longueur_limite_m, vehicule["longueur_m"]),
        (r.poids_limite_t, vehicule["poids_max_t"]),
    ]
    definies = [(limite, valeur) for limite, valeur in limites if limite is not None]
    return not definies or any(valeur > limite for limite, valeur in definies)

@router.get("/")
def liste_restrictions(db: Session = Depends(get_db)):
    return db.query(Restriction).filter(Restriction.actif.is_(True)).all()

@router.get("/profil/{profil}")
def restrictions_par_profil(
    profil: str,
    hauteur_m: float | None = Query(None, gt=0, le=6),
    largeur_m: float | None = Query(None, gt=0, le=4),
    longueur_m: float | None = Query(None, gt=0, le=30),
    poids_max_t: float | None = Query(None, gt=0, le=60),
    db: Session = Depends(get_db),
):
    if profil not in VEHICLE_PROFILES:
        raise HTTPException(status_code=404, detail="Profil véhicule inconnu")
    vehicule = dict(VEHICLE_PROFILES[profil])
    for key, value in {
        "hauteur_m": hauteur_m,
        "largeur_m": largeur_m,
        "longueur_m": longueur_m,
        "poids_max_t": poids_max_t,
    }.items():
        if value is not None:
            vehicule[key] = value
    lignes = db.query(Restriction).filter(Restriction.actif.is_(True)).all()
    applicables = [r for r in lignes if _profil_concerne(r.profils_csv, profil) and _declenchee(r, vehicule)]
    return {
        "profil": profil,
        "vehicule": vehicule,
        "restrictions": applicables,
        "verification_routage": (
            "hgv_beta_non_certifie"
            if profil in {"bus", "utilitaire", "camping_car", "poids_lourd"}
            else "indicative"
        ),
        "message": (
            "Routage grand véhicule en bêta : le gabarit est transmis au moteur HGV quand disponible, mais la validation terrain reste indispensable."
            if profil in {"bus", "utilitaire", "camping_car", "poids_lourd"}
            else
            "Restrictions issues des données AllRoads disponibles ; validation terrain recommandée."
        ),
    }

@router.get("/{restriction_id}")
def element_par_id(restriction_id: int, db: Session = Depends(get_db)):
    element = db.query(Restriction).filter(Restriction.id == restriction_id).first()
    if element is None:
        raise HTTPException(status_code=404, detail="Restriction introuvable")
    return element
