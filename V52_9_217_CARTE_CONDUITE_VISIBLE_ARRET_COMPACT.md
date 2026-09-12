# V52.9.217 — Carte Conduite visible + ARRÊT compact

Base : J216 validée pour tournée directe et géométrie caméra J215.

## Contrôle avant correction
- En paysage, la couche de fond est bien visible.
- En portrait après bascule/cadrage, la route et les overlays peuvent rester visibles alors que les tuiles de fond ne se repeignent pas correctement.
- Le bouton ARRÊT flottant Bus (72 px) empiète visuellement sur la zone basse.

## Correction propre
- Aucune modification du calcul géométrique de caméra J215.
- Après chaque application de caméra : `invalidateSize`, vérification de la couche active, puis `redraw` des tuiles.
- Après changement d'orientation en Conduite : deux rafraîchissements différés courts pour laisser le viewport Android se stabiliser.
- Bouton ARRÊT flottant ramené de 72 px à 60 px, texte 12 px.
- GPS, routage, tournée, clavier J214 et préférences trajet inchangés.
