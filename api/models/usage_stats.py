from sqlalchemy import Boolean, Column, DateTime, Float, String
from db import Base


class UsageSession(Base):
    """Session d'utilisation pseudonymisée, sans donnée géographique."""

    __tablename__ = "usage_sessions"

    id = Column(String(36), primary_key=True)
    user_hash = Column(String(64), nullable=False, index=True)
    profile = Column(String(32), nullable=False, index=True)
    mode = Column(String(24), nullable=False, default="navigation", index=True)
    started_at = Column(DateTime, nullable=False, index=True)
    last_seen_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    active_seconds = Column(Float, nullable=False, default=0.0)
    qualified = Column(Boolean, nullable=False, default=False, index=True)
