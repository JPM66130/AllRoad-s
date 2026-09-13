# J243 — reprise démarrage WP35

- Cause isolée : conflit d’état entre l’ancienne classe `ar-mobile-nav-open` restaurée au lancement et l’autorité Virage Serré `vs-driving-visible`.
- Si la navigation historique était restaurée sans `vs-driving-visible`, l’ancienne couche masquait l’Accueil tandis que Virage Serré masquait la Conduite : seule la couleur de fond restait visible.
- J243 réconcilie l’état au démarrage : hors Conduite explicitement validée, l’Accueil est l’autorité visible.
- Aucun changement GPS, routage, caméra ou logique métier.
