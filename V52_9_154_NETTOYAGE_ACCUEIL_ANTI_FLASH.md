# V52.9.155 — Nettoyage accueil anti-flash

Objectif : supprimer l'apparition fugitive de fenêtres résiduelles lors de l'ouverture de l'accueil.

Cause : l'accueil devenait autoritaire seulement au `window.load`, laissant une courte fenêtre de rendu aux anciennes briques.

Correction :
- `body` démarre avec `ar-mobile-home-open` ;
- un garde CSS masque les autres briques mobiles dès le premier rendu ;
- le JavaScript existant reprend ensuite normalement la main.

Périmètre protégé : GPS, routage, caméra, conduite et ruban non modifiés.
