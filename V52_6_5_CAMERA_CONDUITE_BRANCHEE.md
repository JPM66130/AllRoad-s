# AllRoad's V52.6.5 — Caméra conduite branchée

Correction issue du test réel WP35 : V52.6.4 tournait seulement les tuiles et le tracé, mais pas le plan des marqueurs. La géométrie et le véhicule se désynchronisaient visuellement.

V52.6.5 fait tourner ensemble les plans géographiques Leaflet (fond, tracé, marqueurs, ombres et infobulles), puis contre-tourne uniquement le véhicule neutre pour qu'il reste orienté vers le haut. La caméra choisit le trajet affiché comme référence, place son centre en avant du véhicule et force un zoom conduite.

Démarrer et Démo sans GPS passent par la même fonction `focusDrivingRoute()`. Le mécanisme route bloquée / retournement / reprise n'est pas modifié.
