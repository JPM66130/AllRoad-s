# V52.9.235 — Nettoyage fantômes simulation

- Audit du chemin « Démo sans GPS ».
- Cause racine : le bouton accueil lançait directement `demoDirect` et contournait le clavier JEPALYS.
- Le mode simulation passe désormais par la même saisie et la même comparaison d’itinéraires que la navigation réelle.
- Une seule divergence après calcul : `startSimulationDirect()` remplace la source GPS réelle par la progression simulée sur `routeLayer`.
- Le moteur synthétique historique reste archivé mais n’est plus appelé depuis Virage Serré.
- J227 reste la base de secours propre ; J229/J230 restent les expériences perspective archivées.
