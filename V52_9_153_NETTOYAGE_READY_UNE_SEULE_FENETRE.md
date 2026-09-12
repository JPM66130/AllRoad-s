# V52.9.155 — Nettoyage READY / une seule fenêtre

Cause racine confirmée : `panel("ready")` conserve volontairement `data-state="prepare"` et utilise `data-route-phase="ready"` comme état logique. Des règles historiques V145/V147 forçaient encore le contenu Préparer visible via `data-route-phase`.

Correction : autorité CSS finale exclusivement basée sur `data-route-phase="ready"`; masque structurel des enfants de préparation en portrait et paysage; résultat READY seul; actions flottantes conservées en paysage.

Aucun changement GPS, géocodage, routage, caméra ou ruban métrique.
