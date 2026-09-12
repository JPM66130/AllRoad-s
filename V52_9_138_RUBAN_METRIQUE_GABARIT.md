# V52.9.138 — Ruban métrique lié au gabarit véhicule

- Base : V52.9.137.
- Le ruban bleu n'utilise plus une largeur fixe de 8 px en vue Prêt/Conduite.
- Largeur de référence = largeur réelle du véhicule renseignée dans « Quel véhicule ? » × 1,05.
- Bus / poids lourd standard : repli 2,55 m ; un gabarit enregistré supérieur (convoi exceptionnel) est respecté.
- Conversion mètres → pixels selon le zoom et la latitude Web Mercator.
- La compensation de rotation tient compte du facteur de couverture afin que la largeur finale reste métrique après rotation.
- Minimum 1 px à grande échelle uniquement pour conserver la visibilité de l'itinéraire.
- Aucun changement GPS, routage, fond satellite ou caméra.
