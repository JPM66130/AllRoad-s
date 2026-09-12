# V52.9.210 — Clavier JEPALYS — correction à la cause

- Audit avant correctif : le clavier V207/V208/J209 était créé comme enfant direct de `body`.
- Cause racine trouvée : la garde d'accueil historique masque volontairement, avec `visibility:hidden!important` et `pointer-events:none!important`, tous les enfants directs de `body` sauf l'Accueil et quelques contrôles. Le clavier JEPALYS faisait donc bien partie du DOM mais était systématiquement masqué sur l'Accueil.
- Nettoyage : suppression complète de la couche tactile J209 et des gestionnaires `pointerdown/click` concurrents.
- Correction unique : le clavier est maintenant monté à l'intérieur de `#allroads-mobile-home`, qui est la surface visible autorisée en mode Accueil.
- Une seule délégation `click` sur l'Accueil ouvre la saisie depuis un input ou son label.
- Z-index du clavier placé au-dessus de la pile Accueil.
- Aucun changement GPS, routage, carte ou Conduite.
