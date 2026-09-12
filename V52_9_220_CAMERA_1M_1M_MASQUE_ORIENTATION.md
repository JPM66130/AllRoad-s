# V52.9.220 — Caméra 1 m / 1 m + masque d’orientation

Base : J219 validée comme essai de borne basse 3 m / 10 m.

## But
- chercher la borne basse extrême de la caméra avec une cible théorique **1 m au-dessus / 1 m derrière** ;
- conserver la borne haute harmonisée ~200 m et le calcul géométrique J215 entre les deux ;
- masquer le voile blanc observé lors du passage portrait ↔ paysage.

## Caméra
Leaflet restant 2D, la hauteur est traduite en échelle métrique via un champ vertical de 60°. Le zoom est plafonné par la résolution réellement supportée par la couche cartographique. Le recul de 1 m sert aussi à abaisser géométriquement le point conducteur dans la zone utile. Aucun grossissement CSS artificiel n’est ajouté.

## Rotation
Un masque sombre JEPALYS plein écran est activé immédiatement pendant la reconstruction d’orientation puis retiré après stabilisation. Le fond HTML / Leaflet reste sombre en permanence.

## Périmètre
Aucun changement du GPS, du calcul d’itinéraire, des tournées, du clavier JEPALYS ou des préférences trajet.

Statut : **à tester par moi sur WP35**, portrait → paysage → portrait, puis conduite à l’arrêt pour juger la borne 1 m / 1 m.
