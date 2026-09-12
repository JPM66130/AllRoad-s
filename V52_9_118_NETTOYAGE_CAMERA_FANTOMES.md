# V52.9.118 — Nettoyage caméra / chasse aux fantômes

- Base : V52.9.117.
- Suppression du `scale(1.18)` caché dans la rotation des panes Leaflet.
- Nettoyage des transforms AVANT les calculs de caméra.
- Une seule fonction applique centre + zoom + orientation.
- Même axe local de route utilisé pour orientation et décalage du centre.
- Aucune ancre conducteur dérivée du départ de route sans GPS réel.
- Aucun changement GPS/géocodage/routage.
