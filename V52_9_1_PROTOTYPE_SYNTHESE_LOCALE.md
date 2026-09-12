# AllRoad's V52.9.1 — Prototype synthèse locale

Objectif unique du test : vérifier sur WP35 que la vue de conduite peut être produite localement par le canvas WebGL déjà embarqué dans AllRoad's.

- suppression forcée des anciennes photos cinématiques en conduite Démo sans GPS ;
- le canvas WebGL devient le décor de conduite prioritaire ;
- route, ruban, véhicule et trafic sont produits dans le même repère géométrique ;
- animation plafonnée à environ 20 images/s ;
- aucune API graphique supplémentaire, aucune génération distante, aucun coût par image ;
- les fonctions AllRoad's existantes restent présentes autour du prototype.

Critère du premier test : au clic sur Démarrer, aucune image Nice/Monaco ne doit apparaître. La scène synthétique doit être visible immédiatement.
