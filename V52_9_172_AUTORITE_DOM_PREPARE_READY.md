# V52.9.172 — Autorité DOM PREPARE / READY

- Base : V171 validée au démarrage sur WP35.
- Modification unique : `panel(state)` impose directement au DOM quelle partie itinéraire est visible.
- PREPARE : commandes de préparation visibles, résultat READY masqué.
- READY : préparation masquée, résultat itinéraire visible.
- Une règle finale protège l’attribut `hidden` contre les anciennes règles CSS `!important`.
- GPS, routage, carte, caméra et accueil non modifiés.
