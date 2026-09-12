from sqlalchemy import Boolean, Column, Float, Integer, String
from db import Base

class Restriction(Base):
    __tablename__ = "restrictions"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False, default="information")
    description = Column(String, nullable=False)
    profils_csv = Column(String, nullable=False, default="tous")
    hauteur_limite_m = Column(Float, nullable=True)
    largeur_limite_m = Column(Float, nullable=True)
    longueur_limite_m = Column(Float, nullable=True)
    poids_limite_t = Column(Float, nullable=True)
    niveau = Column(String, nullable=False, default="info")
    actif = Column(Boolean, nullable=False, default=True)
