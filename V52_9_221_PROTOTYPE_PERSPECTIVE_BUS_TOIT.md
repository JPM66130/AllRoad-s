# V52.9.221 — Prototype perspective Bus « assis sur le toit »

## Audit / nettoyage avant correctif
- Base : J220.
- Constat : Leaflet reste une carte 2D ; les essais 1 m / 1 m ne peuvent pas produire une vraie profondeur physique.
- Suppression du masque gris d’orientation J220.
- Abandon de la borne artificielle 1 m / 1 m comme objectif visuel.
- Le moteur Leaflet, le GPS, le routage et les alertes restent intacts comme secours.

## Prototype isolé
- Ajout d’un rendu MapLibre GL uniquement en Conduite Bus réelle.
- Chargement dynamique : aucun changement de technologie globale de l’application.
- Fond satellite raster, itinéraire réel réutilisé, aucun second calcul d’itinéraire.
- Caméra physique de référence Bus : 13 m x 2,55 m x 2,45 m.
- Position de l’œil : environ 3,25 m du sol, près de l’arrière du toit.
- Référence longitudinale provisoire : GPS ramené sur la route = centre du véhicule ; caméra à 5,5 m derrière ce centre.
- Regard : point de route à environ 45 m devant le véhicule.
- Marqueur Bus temporaire pour contrôler l’alignement ; modèle 3D dédié non encore engagé.

## Sécurité de reprise
Si MapLibre/WebGL/CDN ne charge pas, JEPALYS revient automatiquement au rendu Leaflet existant.
Aucun impact sur le calcul d’itinéraire, les tournées, le GPS, les alertes ou l’accueil J214.

## Test WP35
Bus -> Tournée -> Conduite. Vérifier d’abord l’alignement route / véhicule et la profondeur dans les deux orientations.
