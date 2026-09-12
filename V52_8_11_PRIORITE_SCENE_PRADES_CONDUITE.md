# V52.8.11 — Priorité scène Prades en conduite

Correction ciblée après validation WP35 de V52.8.10.

- La scène Prades/Vernet est désormais appliquée directement au fond de la carte avec priorité `!important`.
- L'ancien décor témoin `cinematic_drive_demo.jpg` ne peut plus reprendre la main au passage « Itinéraire prêt → Conduite ».
- Les changements de scènes du scénario (Prades, N116, bouchon, virage, Vernet, blocage, demi-tour, retour) utilisent la même priorité.
- La scène inline est nettoyée lorsqu'on quitte ce scénario afin de ne pas contaminer les autres profils/itinéraires.
- Le reste du comportement V52.8.10 est conservé.
