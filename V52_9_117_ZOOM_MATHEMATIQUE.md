# V52.9.117 — Zoom mathématique de conduite

- Base : V52.9.116.
- Le point conducteur reste verrouillé à X=50 % / Y=72 % de la taille réelle de la carte.
- Le niveau de zoom n'est plus choisi par incréments manuels.
- AllRoad's mesure la hauteur réelle de la carte et réserve la zone utile entre 22 % et 72 % pour la route devant le conducteur.
- L'horizon de route est calculé à partir du trajet restant : 65 % du restant, borné entre 2,5 km et 9 km.
- Pour chaque niveau de zoom candidat (11 à 17), AllRoad's projette la géométrie réelle de l'itinéraire et choisit le niveau dont la longueur affichée est la plus proche de la hauteur utile calculée.
- Orientation : logique précédente conservée.
- Véhicule final : toujours non posé à cette étape.
- GPS, géocodage et routage : inchangés.
