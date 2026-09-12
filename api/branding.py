"""Branding B2B AllRoad's — architecture commune, sans fork client.

La V52.9.31 pose le contrat de configuration. Aucun branding client n'est actif
par défaut : le comportement et l'identité AllRoad's restent inchangés tant
qu'une configuration validée n'est pas fournie.
"""
from dataclasses import asdict, dataclass
from typing import Literal

BrandingMode = Literal["none", "vehicle", "header", "both"]

BRANDABLE_PROFILES = ("voiture", "utilitaire", "camping_car", "bus", "poids_lourd")

@dataclass(frozen=True)
class BrandingConfig:
    client_id: str = ""
    client_name: str = ""
    mode: BrandingMode = "none"
    profiles: tuple[str, ...] = BRANDABLE_PROFILES
    header_label: str = ""
    header_logo: str = ""
    vehicle_logo: str = ""

    @property
    def header_enabled(self) -> bool:
        return self.mode in {"header", "both"}

    @property
    def vehicle_enabled(self) -> bool:
        return self.mode in {"vehicle", "both"}

    def public_dict(self) -> dict:
        data = asdict(self)
        data["header_enabled"] = self.header_enabled
        data["vehicle_enabled"] = self.vehicle_enabled
        data["display_name"] = (
            f"AllRoad's pour {self.client_name}" if self.header_enabled and self.client_name else "AllRoad's"
        )
        return data

DEFAULT_BRANDING = BrandingConfig()

def validate_branding(config: BrandingConfig) -> BrandingConfig:
    if config.mode not in {"none", "vehicle", "header", "both"}:
        raise ValueError("Mode de branding inconnu")
    unknown = set(config.profiles) - set(BRANDABLE_PROFILES)
    if unknown:
        raise ValueError(f"Profils non personnalisables: {', '.join(sorted(unknown))}")
    if config.mode != "none" and (not config.client_id.strip() or not config.client_name.strip()):
        raise ValueError("Un branding actif exige un identifiant et un nom client")
    return config
