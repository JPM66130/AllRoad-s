# V52.9.218 — Caméra Conduite : niveau harmonisé

Objectif : que portrait et paysage donnent la sensation d'être à la même hauteur au-dessus du véhicule.

- Référence commune : environ 0,90 m/pixel, soit un zoom voisin de 17 aux latitudes des essais.
- Cette référence s'applique au démarrage / à très basse vitesse dans les deux orientations.
- En mouvement, la caméra reprend le calcul géométrique dynamique de J215.
- Pendant une rotation, le zoom déjà affiché est conservé brièvement pour éviter un saut visuel.
- Si le GPS devient momentanément non frais pendant la rotation, la caméra garde son dernier cadrage au lieu d'afficher l'ensemble du trajet.
- Aucune position GPS ancienne n'est réutilisée pour le routage ou le guidage.
