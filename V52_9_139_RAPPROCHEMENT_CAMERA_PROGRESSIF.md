# V52.9.139 — Rapprochement caméra progressif

## But
Rapprocher la vue Conduite maintenant que le ruban métrique V138 est crédible, sans toucher au GPS, au routage, au gabarit ni à la largeur du ruban.

## Autorité géométrique
L’horizon visible devant le véhicule est calculé, jamais choisi par un zoom fixe :
- environ 75 secondes de trajet à la vitesse réelle ;
- au minimum la prochaine manœuvre + 25 % de marge de lecture ;
- plancher de 300 m si la distance de manœuvre n’est pas disponible ;
- plafond de 3,2 km.

À l’arrêt avec une prochaine instruction à 450 m, l’horizon cible vaut donc environ 562,5 m au lieu du minimum historique de 1,2 km.

## Périmètre protégé
GPS, géocodage, routage, caméra de placement 50/72, rotation, fond satellite et ruban métrique V138 inchangés.

Statut : à tester sur WP35.
