from sqlalchemy import Boolean, Column, Float, Integer, String
from db import Base

class Alerte(Base):
    __tablename__ = "alertes"
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    message = Column(String, nullable=False)
    profils_csv = Column(String, nullable=False, default="tous")
    niveau = Column(String, nullable=False, default="info")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    source = Column(String, nullable=True)
    actif = Column(Boolean, nullable=False, default=True)
