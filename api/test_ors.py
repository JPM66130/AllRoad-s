"""Smoke test manuel OpenRouteService.

Sans clé ORS locale, ce contrôle externe est explicitement SKIP plutôt qu'en échec :
la suite locale couvre déjà les fallbacks et ne doit pas dépendre d'un secret absent.
"""
from utils.geo import _ors_client


def main():
    client = _ors_client()
    if client is None:
        print("SKIP_ORs: clé OpenRouteService indisponible (smoke test externe non exécuté)")
        return 0

    coords = [[2.621, 42.668], [2.395, 42.55]]
    route = client.directions(coords, profile="driving-car", format="geojson")
    print(route["features"][0]["properties"]["summary"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
