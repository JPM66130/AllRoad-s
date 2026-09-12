# V52.9.183 — Fenêtre de saisie flottante + barres Android stabilisées

## Objectif
- Faire apparaître une fenêtre de saisie JEPALYS juste au-dessus du clavier Android, en portrait et paysage.
- Conserver la validation principale par la touche Entrée/✓ du clavier Android.
- Stabiliser la surface utile de JEPALYS face à l'apparition/disparition des barres système Android.

## Principe clavier
- La fenêtre volante n'apparaît que lorsque `visualViewport` confirme que le clavier est réellement déployé.
- Elle suit le bord supérieur du clavier en portrait et paysage.
- Elle affiche la valeur du champ réellement actif ; la saisie continue dans le champ source.
- Pour Identification et Tournée, la validation via Entrée/✓ reste celle de V181.

## Principe barres Android
- Le lanceur ne modifie aucun réglage Android global.
- Sur appareil tactile/PWA, chaque orientation mémorise la plus petite surface utile observée pendant la session.
- Si les barres Android se masquent, JEPALYS ne s'agrandit plus : pas de saut de composition.
- Si elles apparaissent et réduisent réellement la surface, JEPALYS adopte cette nouvelle limite puis la conserve.
- Sur PC, le redimensionnement de fenêtre reste adaptatif.

## Hors périmètre
GPS, routage, cartographie et logique de conduite inchangés.
