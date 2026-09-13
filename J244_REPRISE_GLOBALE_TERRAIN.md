# J244 — reprise globale terrain WP35

## Contrôle avant correction
- Reproduction source du risque de blocage à la rotation : plusieurs contrôleurs historiques géraient simultanément `resize` / `orientationchange` et figeaient la coque avec des dimensions différentes.
- L'ancien contrôleur PWA `allroads-v52947-pwa-stability` et le verrou `allroads-v52962-single-shell-authority` se chevauchaient avec la caméra et le layout flottant.
- Les observations J243 confirment une carte partielle, une zone bleu pétrole et des commandes inaccessibles après rotation.

## Nettoyage
- Suppression du contrôleur PWA historique concurrent.
- Neutralisation du verrou de coque historique, API de compatibilité conservée.
- Une seule autorité J244 recalcule la coque sur vraie variation de viewport/orientation puis demande le recalage carte/caméra/layout.
- L'autorité anti-écran vide J243 est absorbée dans l'autorité J244, pas empilée comme une rustine supplémentaire.

## Reprise terrain
- Accueil paysage : `Mon véhicule sélectionné` passe sous les 8 vignettes ; fonctions ID/itinéraire restent dans la colonne droite sans chevaucher la carte véhicule.
- Saisie destination : après sélection d'un lieu réel, les touches se rétractent et la place est rendue aux préférences + 3 itinéraires.
- Conduite paysage : panneau de guidage plus haut, panneau 70 km/h agrandi, commandes carte/zoom remises au premier plan, vitesse placée au-dessus des infos trajet.
- Ruban : compromis entre J241 et J242 (`bleu = weight + 1.0`, contour blanc = `weight + 2`).
- Démarrage : l'Accueil reste l'autorité tant qu'une Conduite n'a pas été explicitement validée.

## Validation automatique
- 432 tests passés, 53 historiques ignorés.
- 27 blocs JavaScript inline valides dans chaque frontend.
- Frontends miroir identiques.
- Service workers miroir identiques.
- Compilation Python valide.
