# V52.9.232 — Simulation sans GPS sur le vrai tracé

Objectif : rendre le mode « Démo sans GPS » utile pour valider JEPALYS sur un trajet réel calculé sans rouler.

## Principe
1. Le départ et la destination sont résolus par les services habituels.
2. Le moteur calcule le vrai itinéraire.
3. À réception du trajet, le GPS réel est arrêté pour la simulation.
4. Une position simulée avance sur la géométrie réelle de `routeLayer`.
5. La durée de lecture reprend `duree_min` du trajet calculé.
6. La caméra, le ruban, le guidage et le véhicule utilisent cette position simulée explicite.

## Sécurité
- Aucun point de départ n'est inventé : « Ma position » doit d'abord être obtenue normalement pour calculer l'itinéraire.
- Le mode réel conserve l'autorité GPS fraîche et fiable.
- Aucun MapLibre/Cesium/service 3D payant n'est ajouté.

## Test cible
Voiture → Ma position → Vinça → Démo sans GPS. Vérifier que la voiture suit le vrai tracé et que le ruban/caméra restent cohérents pendant toute la simulation.
