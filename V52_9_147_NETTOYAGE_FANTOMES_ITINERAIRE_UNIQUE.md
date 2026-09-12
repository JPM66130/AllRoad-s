# V52.9.147 — Nettoyage fantômes / itinéraire unique

Constat : V145/V146 conservaient encore le bloc « ready » comme `.ar51-state-panel`, donc il restait lié à l'ancien système de vues et à de nombreuses règles CSS historiques ciblant `[data-state="ready"] .ar51-state-panel[data-panel="ready"]`.

Correction : le résultat « Itinéraire prêt » est désormais physiquement inclus dans le panneau PREPARE et porte la classe dédiée `.ar51-ready-inline`. Ce bloc n'est plus une vue gérée par le contrôleur de panneaux. L'état métier `ready` reste conservé pour le moteur, la caméra et les boutons, mais visuellement il ne provoque plus de changement de panneau.

Aucun changement GPS, géocodage, calcul d'itinéraire, caméra de conduite ou ruban métrique.
