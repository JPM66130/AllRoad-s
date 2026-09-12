# AllRoad's V52.6.8 — Caméra conduite HUD

Objectif unique : reproduire le rendu de conduite validé sans zone grise pendant la rotation Leaflet.

- Démo sans GPS et Démarrer utilisent la même fonction `focusDrivingRoute()`.
- Fond, tracé et géographie tournent ensemble vers le cap.
- Agrandissement géographique limité à 1.46 (couverture des coins pendant rotation).
- Zoom Leaflet ramené à 16 pour compenser cet agrandissement visuel.
- Véhicule conducteur indépendant de Leaflet, fixe au tiers inférieur de la carte.
- Les anciens marqueurs véhicule Leaflet sont masqués uniquement pendant la caméra conduite.
- Aucun logo constructeur.
- L'exploration manuelle puis retour automatique restent conservés.
