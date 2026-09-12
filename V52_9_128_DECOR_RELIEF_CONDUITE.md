# V52.9.128 — Décor Relief en conduite

## Objectif
Tester le rendu de la vue Conduire sur un fond cartographique Relief, sans modifier la caméra ni la chaîne GPS/routage.

## Modification isolée
- La couche temporaire utilisée par la caméra de conduite passe de CARTO Light sans labels à OpenTopoMap (relief/topographie).
- `keepBuffer: 5` est conservé pour le chargement des tuiles autour de la zone visible.
- Aucune modification de la caméra, du zoom, de l’horizon, de l’orientation, du GPS, du géocodage ou du routage.

## Test WP35
Entrer dans Conduire et juger uniquement le décor Relief et la lisibilité du ruban bleu/HUD.
