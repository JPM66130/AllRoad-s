# AllRoad's V52.6.15 — Route sous les roues

Objectif unique : conserver le véhicule exactement sur le tracé après rotation/recentrage.

Correction : l'origine CSS des panes Leaflet n'est plus calculée à partir de rectangles déjà transformés. La caméra précédente est retirée, le layout est recalculé, puis toutes les panes reçoivent la même origine écran (69 % de la hauteur) avant la nouvelle rotation.

Le zoom rapproché V52.6.13 est conservé. Aucun changement volontaire de taille du véhicule ou d'épaisseur du tracé.
