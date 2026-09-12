# V52.9.120 — Référentiel géométrique caméra

- La caméra de conduite utilise désormais un seul référentiel géométrique.
- Le rectangle utile de carte est mesuré à partir de la taille réelle du viewport cartographique et des incrustations hautes/basses.
- Le point conducteur est calculé à 50 % de la largeur utile et 72 % de la hauteur utile.
- Le centre Leaflet est calculé par inversion mathématique de la rotation : la position GPS doit tomber au point conducteur après rotation, sans décalage empirique.
- GPS, géocodage et routage inchangés.
