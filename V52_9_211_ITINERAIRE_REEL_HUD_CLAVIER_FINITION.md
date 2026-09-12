# V52.9.211 — Itinéraire réel affiché + finition clavier JEPALYS

- Audit avant correctif : le calcul réel était bien lancé depuis « Ma position » vers la destination, mais la coque Conduite conservait des valeurs statiques de démonstration (`11,8 km`, `15 min`, `22:28`).
- Correction à la cause : la distance restante, la durée et l’heure d’arrivée de la coque mobile sont maintenant alimentées par `lastCalculatedData`, c’est-à-dire le résultat du moteur de routage réellement reçu.
- Pendant la conduite GPS, la distance restante est recalculée avec `routeProgressAt()` et le temps restant suit la proportion réellement parcourue.
- La prochaine instruction et sa distance sont synchronisées avec le guidage GPS réel.
- Aucun raccourci géographique, aucune coordonnée forcée et aucune route de démonstration ne sont utilisés par « Démarrer ». « Démo sans GPS » reste séparée.
- Finition demandée : logo JEPALYS ajouté au clavier intégré et fond rendu plus translucide pour laisser deviner l’écran sous-jacent.
