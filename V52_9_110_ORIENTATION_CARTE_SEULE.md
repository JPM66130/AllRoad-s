# V52.9.110 — Orientation carte seule

Objectif : première étape des pré-tests de la vue véhicule.

Ordre figé : orientation -> zoom -> véhicule.

Cette version ne modifie que l'orientation visuelle de la carte en conduite :
- le cap est dérivé de la géométrie réelle de l'itinéraire ;
- si une position GPS réelle est disponible, le segment situé devant elle sert de direction ;
- sinon, le début réel de l'itinéraire sert uniquement à orienter la carte, sans inventer de position conducteur ;
- le zoom courant est conservé ;
- aucun recentrage/cadrage véhicule n'est ajouté ;
- le véhicule HUD est volontairement masqué jusqu'à l'étape 3.

GPS, géocodage et calcul d'itinéraire : inchangés.
