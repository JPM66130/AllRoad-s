# AllRoad’s V52.9.5 — optimisation du moteur synthétique

Bloc réalisé après validation vidéo sur WP35.

- banc local conservé : `/app/synth-test.html`
- cible portée à 24 images/s
- rendu interne fixé à 1 pixel physique par pixel CSS pour réduire la charge GPU/mémoire
- arrière-plan statique pré-calculé hors boucle d’animation
- géométrie de route calculée une seule fois par image puis réutilisée pour chaussée, ruban et marquages
- pas de dépendance réseau ni d’API graphique
- bus générique sans logo, toujours ancré sur la même géométrie que le ruban
- réduction du nombre de segments et poteaux sans changer le principe visuel

Objectif de cette version : mesurer le gain de fluidité sur le WP35 avant enrichissement graphique et intégration définitive dans l’assistant de conduite.
