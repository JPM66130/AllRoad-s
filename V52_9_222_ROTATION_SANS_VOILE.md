# V52.9.222 — Rotation sans voile

Base : J221.

## Contrôle avant correction
- Le prototype perspective J221 reste isolé et conserve Leaflet comme secours.
- Le voile observé à la rotation n'est pas un masque J221 : il apparaît pendant la reconstruction/redimensionnement du fond cartographique Leaflet.
- Les animations de tuiles/zoom pouvaient accentuer l'apparition du fond du conteneur pendant cette phase.

## Nettoyage / correction unique
- Aucun nouveau rideau blanc, gris ou opaque.
- Avant une vraie rotation, JEPALYS duplique uniquement le dernier rendu DOM de la carte dans une couche visuelle inerte.
- Cette couche reste affichée pendant que la nouvelle orientation reconstruit la carte, puis disparaît dès que le nouveau rendu a eu le temps de se stabiliser.
- Fond de sécurité sombre JEPALYS sur html/body/carte.
- Animations Leaflet de fondu/zoom désactivées pour éviter les images intermédiaires claires.

## Hors périmètre
GPS, itinéraire, tournée, alertes, Accueil J214 et géométrie caméra ne sont pas modifiés.

Statut : à tester sur WP35, portrait ↔ paysage ↔ portrait.
