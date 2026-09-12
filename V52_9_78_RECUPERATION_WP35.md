# AllRoad's V52.9.79 — Récupération WP35

Objectif : corriger les constats WP35 de V52.9.77 sans ajouter de rustine dans index.html.
Toutes les corrections visuelles de cette passe sont regroupées dans `frontend/allroads_ui_final.css` et son miroir API.

## Corrections
- Mode Nuit : suppression du fond opaque appliqué à `#ar-mobile-nav`, qui se trouvait au-dessus de la carte et masquait entièrement la scène. La coque reste transparente ; la scène utilise sa palette nuit et un voile léger indépendant.
- Conduite portrait : bandeau de manœuvre réduit à 58 px ; distance et instruction sont placées sur une seule ligne compacte.
- Préparer / Itinéraire prêt paysage : même gabarit standard de 82 px ; commandes ramenées à 43 px.
- Véhicule : suppression du doublon de profil dans l'en-tête ; une seule pastille Bus avec LED verte près du titre. L'ensemble est légèrement abaissé en paysage et la carte sélectionnée gagne de l'air en portrait.
- Compteur et logique sécurité non modifiés.

## Cause Nuit identifiée
Dans V52.9.77, `#map` est à un niveau inférieur à `#ar-mobile-nav`. Le thème Nuit imposait un fond `#07111d` au conteneur `#ar-mobile-nav`, couvrant donc le canvas de conduite. Le bref affichage visible pendant une rotation correspond au moment précédant la réapplication du thème. V52.9.79 garde le conteneur transparent.

## Validation automatique
- Suite pytest complète : 201 tests verts.
- JavaScript inline : 18 scripts x 2, syntaxe Node valide.
- JS externe UI : syntaxe valide.
- Miroirs frontend / api/frontend : identiques pour index, CSS d'autorité, JS d'autorité et service worker.
