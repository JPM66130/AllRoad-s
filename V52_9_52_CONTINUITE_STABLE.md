# AllRoad’s V52.9.53 — Continuité conducteur et stabilité PWA

- La PWA installée fige désormais la hauteur de coque entre deux rotations : les micro-`resize` Android/scrcpy ne redimensionnent plus l’interface.
- `visualViewport` est réservé au clavier et ne pilote jamais la coque principale.
- Dans `Itinéraire prêt`, `Modifier` passe à gauche et `Démarrer` à droite pour conserver la continuité du geste conducteur.
- En portrait, la confirmation `Continuer vers l’itinéraire` termine la vue véhicule : aucun grand vide n’est laissé sous le CTA.
- La marge basse standard V52.9.50 reste inchangée.
