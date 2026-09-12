# AllRoad's V52.9.82 — récupération automatique du cadre

## Objectif
Conserver l'adaptation universelle validée en V52.9.81 tout en empêchant une mauvaise manipulation, un zoom tactile ou une variation transitoire des barres Android de faire dériver la composition.

## Règles
- Une vraie rotation ou un vrai redimensionnement de fenêtre déclenche l'adaptation.
- Le `visualViewport` (zoom/pincement/barres système) n'est plus une autorité de géométrie.
- Sur mobile/PWA, les micro-resizes de même orientation sont ignorés.
- Sur PC, un redimensionnement stable de la fenêtre est accepté automatiquement.
- Accueil et Caractéristiques conservent leur cadre ; les images utilisent `object-fit: cover` et peuvent être recadrées dans leur fenêtre, sans réduire la coque.
- Après 4 s d'inactivité, un garde-cadre remet automatiquement la page à l'origine si un scroll/zoom parasite a déplacé la vue, sans interrompre une saisie active ni un état critique de conduite.
- Le zoom navigateur tactile accidentel est bloqué par le viewport applicatif (`maximum-scale=1`, `user-scalable=no`).

## ADN
ALLROAD'S — Partout, pour tous ! Une seule application, un seul moteur UI, adaptation automatique au support réel.
