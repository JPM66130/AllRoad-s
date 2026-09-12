# V52.9.180 — Correction navigation accueil / garage

## Cause corrigée
La V179 observait toutes les mutations internes du DOM. Le rendu de la liste des tournées réécrivait lui-même cette liste, ce qui relançait l’observateur en boucle. Conséquence : interface figée, clics inopérants et changement portrait/paysage bloqué.

## Correction
- Observation limitée au changement de classe du `body` : plus de boucle de rendu.
- Les boutons et profils de l’accueil redeviennent utilisables.
- Le passage portrait/paysage redevient réactif.
- Clic sur la zone principale « Mon véhicule sélectionné » : ouverture de « Gérer mes véhicules » directement sur les caractéristiques du véhicule actif.
- « Identification » et « Tournée » conservent leur ouverture ciblée dans la même page.

## Périmètre protégé
Aucune modification du GPS, du routage, de la carte, de la caméra ou de la conduite.
