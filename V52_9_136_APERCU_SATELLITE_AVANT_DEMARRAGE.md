# V52.9.136 — aperçu Satellite avant démarrage

Base : V52.9.135 (application V132 + lancement système stabilisé).

Passe isolée : état **Prêt** uniquement.
- Satellite temporaire.
- Affichage immédiat de l’itinéraire complet.
- Après 700 ms, si un GPS réel fiable et frais (<= 15 s) existe, animation vers ce GPS au zoom 16.
- Sans GPS frais : aucun point inventé, la vue reste sur l’itinéraire complet.
- Aucun changement GPS, géocodage, routage ou caméra Conduire.
