# V52.9.227 — caméra métrique harmonisée portrait / paysage

Base : J226 nettoyée.

## Contrôle avant correction
- Les captures WP35 montrent la même position GPS et le même itinéraire, mais un niveau/cadrage différent entre portrait et paysage.
- Le fond sombre intermittent pouvait être favorisé par des `redraw()` de tuiles lancés pendant chaque application de caméra/rotation.
- L'ancienne résolution de zoom utilisait les limites en pixels du viewport : le résultat pouvait donc différer selon l'orientation.

## Nettoyage / correction
- Une seule caméra reste autoritaire : `focusDrivingRoute()` -> `arE7ApplyDrivingCamera()`.
- Suppression des `redraw()` destructifs dans la chaîne normale de caméra ; Leaflet conserve les tuiles déjà peintes et charge naturellement les nouvelles après `setView` / `invalidateSize`.
- Le zoom de conduite est maintenant déterminé par une formule métrique commune (latitude + horizon réel), indépendante du ratio portrait/paysage.
- En rotation, le zoom déjà appliqué est conservé exactement.
- Le véhicule reste ancré au même pourcentage de la zone utile ; seule la découpe horizontale/verticale change avec le support.

## Hors périmètre
Aucun changement GPS, routage, tournées, Accueil, préférences ou alertes.
