# V52.9.76 — correction WP35 à la cause

- Zoom Leaflet natif désactivé directement dans `L.map(..., {zoomControl:false})`, avec filet CSS global.
- Titre véhicule forcé sur une ligne à 20 px sur WP35 portrait.
- Renfort immersif : sur geste utilisateur, demande Fullscreen API avec `navigationUI: hide` quand disponible.
- Limite assumée : Android reste maître de ses barres système ; une PWA web ne peut pas garantir leur suppression permanente.
- L’ordre conduite validé V60 reste inchangé.
