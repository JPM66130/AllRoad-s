# V52.9.129 — Rotation : couverture géométrique du viewport

- Base : V52.9.128.
- Audit ciblé des bandes haut/bas visibles après rotation de la carte.
- Cause retenue : depuis la suppression du `scale(1.18)` arbitraire en V52.9.118, les panes Leaflet sont tournées sans surdimensionnement calculé ; suivant l'angle et le ratio du viewport, les coins du rectangle écran peuvent donc sortir de la surface couverte.
- Correction : facteur de couverture calculé exactement à partir de la largeur, de la hauteur et de l'angle de rotation.
- Ce facteur est compensé dans le calcul du centre et dans le test de zoom : il ne constitue donc plus un « zoom caché ».
- Caméra, horizon dynamique, GPS, géocodage, routage, ruban bleu et décor relief conservés.
