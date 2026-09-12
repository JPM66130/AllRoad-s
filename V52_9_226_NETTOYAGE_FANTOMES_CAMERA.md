# V52.9.226 — Nettoyage des fantômes caméra

Base : J225.

## Audit
Plusieurs autorités historiques pouvaient encore agir autour de Conduite :
- prototype MapLibre J221 chargé dynamiquement et capable de masquer Leaflet ;
- gel/clone de carte J222 pendant les rotations ;
- mode caméra historique `driver/overhead` mémorisé dans `localStorage` ;
- anciens noms de classes caméra 5265/5266/5267 encore manipulés sans autorité CSS active.

## Nettoyage
- retrait complet du prototype perspective J221 et de ses CSS/chargements CDN ;
- retrait du clone d'orientation J222 ;
- suppression du choix `overhead` persistant : Conduite possède une seule caméra active ;
- conservation d'une seule chaîne `focusDrivingRoute()` -> `arE7ApplyDrivingCamera()` ;
- rotation : simple invalidation de surface + stabilisation par cette même autorité ;
- aucun changement GPS, itinéraire, gabarit, tournée ou Accueil.

## But du test WP35
Vérifier que portrait/paysage conservent le fond satellite, le même point véhicule et le même cadrage sans bascule parasite.
