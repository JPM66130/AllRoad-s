# V52.9.109 — Vue véhicule pré-tests

- Base : V52.9.108 nettoyée.
- But unique : obtenir une vraie vue véhicule exploitable avant les pré-tests routiers.
- Le véhicule HUD n'est affiché qu'après disponibilité d'une position GPS réelle ; aucune position n'est inventée.
- Caméra conduite : ancrage véhicule vers 72 % de la hauteur, cap donné par la route devant le fix, zoom 17 à basse vitesse, 16 à partir de 50 km/h, 15 à partir de 90 km/h.
- Le mode vue dessus conserve son comportement séparé.
- GPS, géocodage, géométrie d'itinéraire, vitesse et alertes inchangés.
- Le jeton `ui=vehicle109` force le WP35 à ouvrir la nouvelle interface sans casser les contrôles historiques du lanceur.
- Statut : à tester par Jean-Paul sur WP35.

- Contrôles : 304 tests réussis ; 20 scripts JavaScript inline valides ; miroirs frontend identiques.
