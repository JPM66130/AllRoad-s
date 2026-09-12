# V52.9.126 — Nettoyage autorité guidage

## Cause démontrée
La V52.9.125 modifiait `allroads_ui_final.css`, mais la feuille est chargée avant le bloc inline `ar529108-driving-clean-hud` dans `index.html`. Ce bloc, déclaré autorité visuelle unique de Conduire, réimposait ensuite `background: rgba(10,39,52,.91)`, bordure et ombre sur `.ar51-maneuver`. La transparence V125 ne pouvait donc pas gagner la cascade CSS.

## Nettoyage
- suppression du bloc V125 devenu une seconde autorité inefficace ;
- modification de l'autorité V108 elle-même ;
- fond guidage ramené à 18 % d'opacité, sans bordure ni ombre, léger flou 2 px ;
- contenu (flèche, distance, instruction, limitation) inchangé ;
- caméra/GPS/routage inchangés.
