# V52.9.119 — Autorité caméra / GPS frais

Objectif : identifier et supprimer les dernières sources de pseudo-position pouvant empêcher la caméra de conduite de s'appliquer proprement.

- La caméra de conduite lit désormais directement un fix GPS fiable et frais (<= 15 s).
- `vehicleMarker` et `mobileDriveMarker` ne sont plus des autorités de position : ce sont uniquement des rendus visuels.
- À l'entrée en conduite réelle, tout ancien `mobileDriveMarker` est supprimé avant le démarrage GPS.
- Un état diagnostic `window.AllRoadsCameraAuthority.getState()` indique `waiting-gps`, `waiting-route`, `applied` ou `error`.
- Aucun changement de géocodage, calcul d'itinéraire ou règles de sécurité GPS.
