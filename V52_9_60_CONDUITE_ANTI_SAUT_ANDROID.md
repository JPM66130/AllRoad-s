# V52.9.60 — conduite figée / anti-saut Android
- Ordre conduite renforcé : Header → Carte/Relief/Satellite → bandeau 450 m → carte.
- Sélecteur cartographique prioritaire en z-index et ancré sous le header.
- Coque WP35 monotone par orientation : apparition d'une barre Android ne peut plus réduire la hauteur CSS d'AllRoad's.
- Une vraie rotation réinitialise la référence ; une augmentation de surface utile est acceptée, une réduction transitoire est ignorée.
- Les barres système Android elles-mêmes restent contrôlées par Android ; AllRoad's neutralise leur effet de redimensionnement sur son interface.
