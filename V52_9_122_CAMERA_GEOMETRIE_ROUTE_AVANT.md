# V52.9.122 — Caméra géométrique sur la route devant

- Base : V52.9.121.
- Le ruban bleu #006CFF sans contour gris reste figé.
- Le point conducteur reste calculé dans la zone cartographique utile.
- Le zoom est désormais choisi en projetant la route devant le conducteur dans le repère réellement tourné de la caméra.
- Pour chaque niveau de zoom Leaflet, la boîte englobante de la route avant est comparée au rectangle sûr de l'écran ; le niveau le plus rapproché qui tient est retenu.
- Aucun changement GPS, géocodage ou routage.
