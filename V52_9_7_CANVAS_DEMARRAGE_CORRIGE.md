# V52.9.7 — Canvas de conduite : démarrage corrigé

Correction ciblée du moteur synthétique intégré.

- suppression des séquences `\n` littérales qui rendaient le bloc JavaScript du moteur invalide dans `index.html` ;
- le moteur Canvas peut désormais réellement exécuter son cycle `start → resize → render` au passage en conduite ;
- aucun changement de la préparation du trajet, de l'itinéraire prêt, du HUD, des alertes ni des commandes chauffeur ;
- le rendu reste local et sans service graphique externe.
