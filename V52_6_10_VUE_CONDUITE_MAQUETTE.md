# AllRoad's V52.6.10 — Vue conduite proche de la maquette

Objectif : rapprocher le rendu réel de la maquette de conduite validée.

- caméra plus proche (zoom Leaflet 17)
- véhicule HUD plus présent et plus bas
- perspective légère pour donner de la profondeur à la route
- route bleue avec liseré blanc de conduite
- cap vers le haut et davantage de route devant le véhicule
- bandeau de manœuvre et panneau inférieur recalibrés
- même caméra pour Démarrer et Démo sans GPS
- aucun plein écran automatique

Limite assumée : la maquette illustrative utilisait un rendu de relief quasi-3D. Le moteur Leaflet actuel reste une cartographie 2D ; cette version reproduit la composition et la sensation de conduite sans prétendre transformer les tuiles OSM/Topo/Satellite en véritable moteur 3D.
