from sqlalchemy import Column, Float, Integer
from db import Base


class Compteur(Base):
    __tablename__ = "compteur"

    id = Column(Integer, primary_key=True, default=1)
    total_km = Column(Float, nullable=False, default=0.0)
    trajets = Column(Integer, nullable=False, default=0)
