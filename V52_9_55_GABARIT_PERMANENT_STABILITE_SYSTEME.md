# V52.9.58 — Gabarit permanent + stabilité barre système WP35

- Les caractéristiques du véhicule sont visibles en permanence sur la vue véhicule.
- Au repos, les champs sont en lecture seule ; ils deviennent éditables uniquement via Enregistrer un véhicule, Véhicule occasionnel ou Modifier.
- La sélection d’un véhicule recharge immédiatement ses caractéristiques dans le bloc permanent.
- La coque PWA utilise le grand viewport stable (`lvh`) en mode installé afin que l’apparition transitoire de la barre gestuelle Android ne provoque plus de reflow vertical de l’interface.
- `viewport-fit=cover` et `interactive-widget=overlays-content` complètent la gestion des zones système/clavier.
- Le lanceur est réécrit sans BOM afin que `@echo off` soit effectif sous Windows.
