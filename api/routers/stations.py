import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models.stations import Station

router = APIRouter(prefix="/stations", tags=["Stations"])
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "stations.json"


def _local_stations():
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []


@router.get("/")
def liste_stations(db: Session = Depends(get_db)):
    stations = db.query(Station).all()
    if stations:
        return stations
    return _local_stations()


@router.get("/{station_id}")
def station_par_id(station_id: int, db: Session = Depends(get_db)):
    station = db.query(Station).filter(Station.id == station_id).first()
    if station:
        return station
    for local_station in _local_stations():
        if local_station.get("id") == station_id:
            return local_station
    raise HTTPException(status_code=404, detail="Station introuvable")
