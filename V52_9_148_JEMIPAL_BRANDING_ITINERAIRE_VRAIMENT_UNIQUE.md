# V52.9.148 — JEMIPAL + itinéraire réellement unique

- Nouveau branding JEMIPAL avec logo validé.
- Le logo est intégré à l’accueil, aux en-têtes navigation/véhicule et au lanceur de profils.
- READY n’est plus exposé comme état visuel racine : `data-state` reste `prepare`; la logique est conservée dans `data-logic-state=ready` et l’affichage résultat dans `data-route-phase=ready`.
- Les anciennes règles CSS `[data-state=ready]` ne peuvent donc plus piloter la mise en page.
- Le bloc résultats reste physiquement dans le panneau Préparer.
- GPS, géocodage, routage, caméra et ruban métrique non modifiés.
