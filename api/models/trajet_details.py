from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text

from db import Base


class TrajetDetail(Base):
    __tablename__ = "trajet_details"

    id = Column(Integer, primary_key=True, index=True)
    itineraire_id = Column(Integer, ForeignKey("itineraires.id"), nullable=False, unique=True, index=True)
    nom_tournee = Column(String, nullable=False, default="Tournée sans nom")
    profil = Column(String, nullable=False)
    geometry_json = Column(Text, nullable=False)
    sauvegarde_volontaire = Column(Boolean, nullable=False, default=False)
    statut_diffusion = Column(String, nullable=False, default="personnelle")
    client_id = Column(String, nullable=True)
    depot_id = Column(String, nullable=True)
    validee_par = Column(String, nullable=True)
    note_exploitation = Column(Text, nullable=True)
    tournee_uid = Column(String, nullable=True, index=True)
    version_numero = Column(Integer, nullable=False, default=1)
    version_parent_id = Column(Integer, nullable=True)
    est_version_active = Column(Boolean, nullable=False, default=True)