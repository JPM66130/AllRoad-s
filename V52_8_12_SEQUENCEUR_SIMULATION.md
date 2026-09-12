# AllRoad's V52.8.12 — Séquenceur simulation secteur

Correction ciblée de la simulation Bus Prades → Vernet-les-Bains.

- Les scènes avancent désormais sur une horloge propre à la simulation.
- La progression visuelle ne dépend plus du tracé Leaflet ni du déplacement du marqueur.
- Le véhicule continue de suivre le tracé lorsqu'il est disponible.
- Première scène appliquée immédiatement, puis transitions visibles toutes les 6 à 7 secondes.
- Fin de scénario corrigée : le retour ne s'arrête plus prématurément.
- Cache-buster des images de scène (`?v=52812`) pour éviter la réutilisation d'anciens décors par le navigateur.
- Aucun changement aux 8 profils, au gabarit, au compteur d'utilisation ou à la logique générale de navigation.
