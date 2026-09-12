# V52.9.53 — saisie clavier stable WP35

- La marge basse standard V52.9.50 est conservée sans modification.
- Le champ Départ/Destination actif reste visible au-dessus du clavier Android.
- Le clavier prend temporairement de la place à la carte, jamais au champ actif.
- Un seul contrôleur pilote désormais le viewport principal afin d'éviter les oscillations visuelles.
- `visualViewport` est réservé à la détection du clavier et ne redimensionne plus la coque principale.
- Les heartbeats de session devenus obsolètes après redémarrage serveur répondent proprement en 200 au lieu de générer un faux 404 rouge.

## Validation technique
136 tests verts après correction, puis contrôles ciblés navigation/chauffeur/données route/géographie et vérifications JS/PWA relancés.
