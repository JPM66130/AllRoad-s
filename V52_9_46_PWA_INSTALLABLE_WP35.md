# V52.9.46 — PWA installable WP35

- Corrige les 404 PWA de V52.9.45 : le service worker ne référence plus app.js/style.css inexistants.
- Ajoute une icône favicon locale valide.
- Nettoie les anciens caches de service worker lors de l'activation.
- Conserve le tunnel ADB localhost:8000, nécessaire au contexte local fiable sur le WP35.
- Conserve manifest display fullscreen avec fallback standalone et orientation any.
- Capture l'événement navigateur `beforeinstallprompt` à titre de diagnostic, sans forcer une installation impossible sans geste utilisateur.
