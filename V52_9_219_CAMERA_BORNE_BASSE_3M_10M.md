# V52.9.219 — Caméra Conduite : borne basse 3 m / 10 m

Base : J218 validée pour l’harmonisation portrait / paysage.

- Borne haute conservée : référence visuelle ~200 m / 0,90 m par pixel.
- Borne basse d’essai : caméra conceptuelle 3 m au-dessus et 10 m derrière le véhicule.
- Entre les deux : calcul géométrique J215, sans pas de zoom empirique.

Leaflet est une carte 2D : l’altitude 3 m est convertie en échelle théorique avec un champ vertical de 60°. Si cette échelle dépasse la résolution cartographique disponible, JEPALYS s’arrête au zoom maximal réel (20), sans faux scale CSS. Les 10 m derrière sont convertis en pixels à l’échelle réellement atteinte pour positionner le véhicule.

Le fond clair par défaut de Leaflet est remplacé par le fond sombre JEPALYS pendant une rotation pour supprimer le voile blanc provenant de l’application.

GPS, routage, ruban métrique, tournée directe et clavier J214 inchangés.
