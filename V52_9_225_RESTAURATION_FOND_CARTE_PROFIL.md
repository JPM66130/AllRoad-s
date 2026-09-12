# V52.9.225 — Fond de carte stable lors du changement de profil

## Contrôle avant correction
J224 conserve le gabarit Voiture réel (4,40 × 1,80 × 1,50 m), mais le prototype perspective Bus peut finir son initialisation asynchrone après un changement de profil et réactiver la classe qui masque les panes Leaflet. Cela explique un fond bleu sombre avec seulement le ruban/vehicule visibles.

## Nettoyage / correction
- une séquence unique annule toute initialisation perspective devenue obsolète ;
- chaque activation revalide l'état Conduite + profil Bus après les opérations asynchrones ;
- quitter Bus invalide immédiatement la séquence et rend Leaflet autoritaire ;
- aucun changement GPS, routage, gabarit voiture ou caméra Leaflet.

## Test WP35
Voiture 4,40 × 1,80 × 1,50 m → Conduite → portrait/paysage : fond satellite visible et cadrage rapproché conservé.
