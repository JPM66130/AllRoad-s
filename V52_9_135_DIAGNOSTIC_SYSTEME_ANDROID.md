# V52.9.135 — Diagnostic système Android / barres visibles

Base fonctionnelle : **V52.9.132 validée sur WP35**.

## But unique
Isoler un éventuel mode immersif Android persistant, extérieur à AllRoad’s.

## Modification
- Aucun changement HTML/CSS/JS/Python de l’application.
- Le lanceur ADB lit `settings global policy_control`, l’affiche, puis supprime cette règle globale avant l’ouverture.
- Le test ouvre ensuite l’URL AllRoad’s explicitement dans Chrome si Chrome est présent.
- Aucun paquet n’est désinstallé et aucune donnée AllRoad’s n’est supprimée.

## Test WP35
1. Lancer `AA_LANCER_ALLROADS_V52_9_135.bat`.
2. Regarder les deux lignes `policy_control AVANT` et `policy_control APRES` dans la fenêtre noire.
3. Vérifier si la barre d’état Android (heure/réseau/batterie) et la navigation Android sont visibles.
4. Tester portrait puis paysage uniquement.

Si les barres restent absentes avec `policy_control APRES : null` (ou vide), le fantôme n’est pas la politique immersive globale et il faut poursuivre au niveau activité/ROM WP35.
