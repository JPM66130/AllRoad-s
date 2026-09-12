# V52.9.6 — Moteur synthétique intégré

- Le moteur Canvas2D local est désormais branché directement dans la vue « Conduite en cours ».
- La carte Leaflet reste active en arrière-plan pour la logique, mais ses couches sont masquées visuellement pendant la conduite.
- Le HUD mobile, le guidage, la limitation de vitesse, les statistiques et le signalement de route bloquée restent au-dessus du rendu.
- Le rendu reste local, sans API graphique ni coût récurrent.
- Le ruban bleu et le bus utilisent la même géométrie de voie.
- Sortie de conduite : la carte classique réapparaît automatiquement.
