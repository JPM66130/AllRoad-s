# V52.9.111 — Orientation centrée de la carte

Objectif : corriger l'étape orientation avant de toucher au zoom ou au véhicule.

Constat V52.9.110 :
- la rotation fonctionnait ;
- mais elle était appliquée autour d'un pivot situé à 72 % de la hauteur ;
- ce pivot déplaçait visuellement le trajet hors de la zone utile lors de la rotation.

Correction V52.9.111 :
- rotation autour du centre réel de la carte (50 % / 50 %) ;
- la carte conserve donc son centre pendant la rotation ;
- même calcul de direction à partir de la géométrie réelle de l'itinéraire ;
- aucun changement de zoom ;
- aucun travail de placement véhicule ;
- GPS, géocodage et routage inchangés.

Ordre de travail conservé : orientation -> zoom -> véhicule.
