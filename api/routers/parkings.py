from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.parkings import Parking

router = APIRouter(prefix="/parkings", tags=["Parkings"])

@router.get("/")
def liste_parkings(db: Session = Depends(get_db)):
    return db.query(Parking).all()


@router.get("/{parking_id}")
def element_par_id(parking_id: int, db: Session = Depends(get_db)):
    element = db.query(Parking).filter(Parking.id == parking_id).first()
    if element is None:
        raise HTTPException(status_code=404, detail="Parking introuvable")
    return element
