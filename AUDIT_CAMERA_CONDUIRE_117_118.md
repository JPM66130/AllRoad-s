# Audit caméra Conduire — V52.9.117 → V52.9.118

## Fantômes identifiés

1. **Zoom visuel caché** : `setDrivingBearing()` appliquait `scale(1.18)` aux panes Leaflet en plus du zoom Leaflet. Le calcul mathématique choisissait donc un zoom, puis l'affichage était agrandi de 18 % hors du moteur de carte. Supprimé.
2. **Mesure après transformation précédente** : un nouveau `setView()` pouvait être calculé/appliqué alors que les panes portaient encore la rotation du cadre précédent. Le nettoyage des transforms est maintenant fait avant toute projection et avant le `setView` final.
3. **Deux axes pour un même cadre** : le centrage utilisait un point lointain (horizon) tandis que l'orientation utilisait un segment local (~220 m). Une courbe pouvait donc donner deux directions différentes. Le centre et l'orientation utilisent maintenant le même axe local devant le conducteur.
4. **Position implicite au départ de route** : sans GPS, la caméra mathématique prenait `pts[0]` comme ancre. Cela ressemblait à une position conducteur inventée. Supprimé : sans position réelle, aucune caméra conducteur n'est fabriquée.

## Autorité conservée

`focusDrivingRoute()` reste le seul calculateur de cadre en mode Conduire. `arE7ApplyDrivingCamera()` est désormais l'unique point d'application du couple centre/zoom/orientation pour la caméra conducteur. Les appels GPS, resize et retour après exploration peuvent demander un nouveau cadre, mais ne calculent pas eux-mêmes une caméra concurrente.

## Hors périmètre

GPS, géocodage, calcul d'itinéraire, progression de route et sécurité ne sont pas modifiés.
