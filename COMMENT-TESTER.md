# COMMENT TESTER — J211

1. Lancer `AA_LANCER_JEPALYS.bat`.
2. Vérifier en haut : **J212 · Virage Serré · 2 vues**.
3. Choisir Bus, saisir **Feurs** comme destination puis **Valider** / **Démarrer**.
4. Attendre le calcul réel avant l’ouverture de Conduite.
5. Vérifier que **RESTE** n’affiche plus 11,8 km par défaut : il doit reprendre la distance réellement calculée depuis la position GPS.
6. Vérifier que **TEMPS** et **ARRIVÉE** correspondent au même calcul réel.
7. En mouvement, vérifier que RESTE diminue avec la progression GPS.
8. Ouvrir une saisie : le clavier JEPALYS doit garder son fonctionnement J210, afficher le logo et laisser davantage deviner l’écran en dessous.

## J213 — contrôle WP35
1. Vérifier `J213 · Virage Serré · 2 vues`.
2. Vérifier que Voiture + Bus restent normaux et que les 6 autres profils sont grisés `TEST INTERNE` mais cliquables sur ce banc développeur.
3. Sélectionner un véhicule actif, saisir une destination et choisir les préférences Sans autoroute / Sans péage / Sans ferry.
4. Appuyer sur Démarrer : une comparaison de 3 itinéraires doit apparaître avec km, temps, consommation et coût estimé.
5. Choisir un itinéraire : JEPALYS doit charger ce choix puis passer en Conduite.
6. Cas de contrôle : autoroute autorisée + Sans péage doit rester possible ; aucune autoroute ne doit être assimilée automatiquement à un péage.
