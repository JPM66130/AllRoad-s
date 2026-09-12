# V52.9.124 — Horizon de conduite dynamique

## Objectif
Remplacer le cadrage basé sur une fraction du trajet restant par un horizon de conduite calculé à partir de la vitesse réelle.

## Règle
- fenêtre temporelle : 180 s ;
- horizon minimum : 1 200 m ;
- horizon maximum : 6 500 m ;
- formule : vitesse (m/s) × 180 s, bornée entre 1 200 et 6 500 m ;
- la distance réellement restante ne sert qu'à plafonner l'horizon ;
- le zoom Leaflet reste choisi géométriquement à partir de la projection de cet horizon dans la zone cartographique utile.

## Invariants
Aucun changement GPS, géocodage ou routage. Le ruban bleu #006CFF sans contour gris reste inchangé. Le point conducteur et le référentiel géométrique restent ceux des versions précédentes.
