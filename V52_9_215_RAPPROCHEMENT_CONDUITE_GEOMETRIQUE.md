# V52.9.215 — Rapprochement Conduite géométrique

## Base validée
J214 « grand luxe » reste la référence ergonomique Accueil / clavier JEPALYS.

## But
Rapprocher réellement la vue Conduite sans appliquer un +1/+2 de zoom empirique.

## Autorité de calcul
- point conducteur inchangé : X=50 % de la carte utile, Y=72 % de sa hauteur utile ;
- horizon devant le véhicule : 45 s à la vitesse GPS réelle ;
- prochaine manœuvre prise en compte dans une enveloppe locale, sans forcer une vue lointaine ;
- horizon borné entre 180 m et 1,8 km ;
- la géométrie réelle de cette portion de route est projetée et tournée dans le même repère que la caméra ;
- le zoom maximal admissible est résolu mathématiquement depuis le rectangle sûr de l’écran ;
- pas de delta de zoom arbitraire ; précision Leaflet au quart de niveau.

## Protégé
Aucun changement du GPS, du géocodage, du calcul d’itinéraire, du ruban métrique, de la largeur véhicule ou de l’ergonomie J214.

Statut : **à tester par moi sur WP35 en conduite réelle**.
