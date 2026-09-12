from branding import BRANDABLE_PROFILES, BrandingConfig, validate_branding


def test_branding_profiles_cover_commercial_vehicle_families():
    assert BRANDABLE_PROFILES == ("voiture", "utilitaire", "camping_car", "bus", "poids_lourd")


def test_three_paid_branding_combinations_are_independent():
    vehicle = BrandingConfig(client_id="acme", client_name="ACME", mode="vehicle")
    header = BrandingConfig(client_id="acme", client_name="ACME", mode="header")
    both = BrandingConfig(client_id="acme", client_name="ACME", mode="both")
    assert vehicle.vehicle_enabled and not vehicle.header_enabled
    assert header.header_enabled and not header.vehicle_enabled
    assert both.header_enabled and both.vehicle_enabled
    assert header.public_dict()["display_name"] == "AllRoad's pour ACME"


def test_branding_is_safe_off_by_default():
    cfg = BrandingConfig()
    assert not cfg.header_enabled and not cfg.vehicle_enabled
    assert cfg.public_dict()["display_name"] == "AllRoad's"


def test_active_branding_requires_client_identity():
    try:
        validate_branding(BrandingConfig(mode="both"))
    except ValueError:
        pass
    else:
        raise AssertionError("Un branding actif sans client doit être refusé")


def test_no_unsafe_turnaround_wording_in_routing_errors():
    from pathlib import Path
    text = (Path(__file__).parents[1] / "routers" / "itineraires.py").read_text(encoding="utf-8").lower()
    assert "revenez sur vos pas" not in text
