# V52.9.8 — Moteur synthétique prioritaire et réellement animé

Correction du conflit de couches découvert en V52.9.7.

- l’ancien canvas 3D `ar5271-scene3d` ne peut plus recouvrir le moteur synthétique pendant la conduite ;
- le canvas `ar5296-drive-canvas` devient explicitement le décor prioritaire ;
- démarrage renforcé : détection par `data-state` **ou** par la classe de conduite du `body` ;
- première image rendue immédiatement au démarrage ;
- mouvement longitudinal continu ajouté (courbes, pointillés et poteaux progressent avec le véhicule) ;
- reprise après retour d’onglet / écran et redimensionnement conservée ;
- aucun service graphique externe ajouté.

Objectif test WP35 : vérifier que la route synthétique est visible **et bouge clairement** dès l’entrée en « Conduite en cours ».
