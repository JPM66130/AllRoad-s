from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.spots import Spot

router = APIRouter(prefix="/spots", tags=["Spots"])

@router.get("/")
def liste_spots(db: Session = Depends(get_db)):
    return db.query(Spot).all()


@router.get("/{spot_id}")
def element_par_id(spot_id: int, db: Session = Depends(get_db)):
    element = db.query(Spot).filter(Spot.id == spot_id).first()
    if element is None:
        raise HTTPException(status_code=404, detail="Spot introuvable")
    return element
