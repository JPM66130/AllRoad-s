# V52.9.224 — Stabilisation géométrique du premier rendu Conduite

Base : J222.

## Contrôle avant correction
Les captures WP35 montrent trois états successifs :
1. ouverture portrait avec une zone cartographique incohérente / hors trajet ;
2. rotation paysage qui force un recalcul et retrouve la bonne zone ;
3. retour portrait qui conserve enfin la bonne zone, mais avec un cadrage différent.

La cause est un recalcul de caméra lancé avant stabilisation réelle de la surface utile lors de l'entrée en Conduite. La rotation, elle, provoquait implicitement un second calcul sur une surface déjà stabilisée.

## Nettoyage
- aucune nouvelle autorité GPS ;
- aucune nouvelle autorité d'itinéraire ;
- pas de zoom empirique portrait/paysage ;
- suppression des appels de rafraîchissement concurrents dans le gestionnaire d'orientation J222 au profit d'une seule séquence de stabilisation.

## Correction
Une seule fonction `ar223StabilizeDrivingCamera()` recalcule la taille Leaflet, les tuiles et la caméra après stabilisation de la coque, à l'entrée en Conduite et après une vraie rotation.

Objectif : l'ouverture portrait doit directement montrer la même zone logique que le paysage et le retour portrait, sans nécessiter une rotation pour corriger la caméra.
