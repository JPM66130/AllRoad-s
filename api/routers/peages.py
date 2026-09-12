from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.peages import Peage

router = APIRouter(prefix="/peages", tags=["Péages"])

@router.get("/")
def liste_peages(db: Session = Depends(get_db)):
    return db.query(Peage).all()


@router.get("/{peage_id}")
def element_par_id(peage_id: int, db: Session = Depends(get_db)):
    element = db.query(Peage).filter(Peage.id == peage_id).first()
    if element is None:
        raise HTTPException(status_code=404, detail="Péage introuvable")
    return element
