# V52.9.130 — Stabilisation fond de carte / orientation

Objectif : empêcher un changement de fond de carte lors d'un passage portrait/paysage ou d'une perte GPS momentanée pendant Conduire.

Cause identifiée : `arE7RefreshState()` rappelait systématiquement `arE7EnsureBaseLayer()`, qui rechargeait la vue mémorisée (Carte/Relief/Satellite) avant de rendre la main à la caméra de conduite. En parallèle, `clearDrivingBearing()` restaurait aussi l'ancienne couche lors d'une perte GPS/route momentanée. Le fond de carte était donc couplé à l'état transitoire de la caméra.

Correction : en état Conduire réel, `arE7EnsureBaseLayer()` conserve désormais la couche de conduite. `clearDrivingBearing()` ne restaure plus le fond par défaut ; la restauration n'a lieu qu'en quittant réellement l'état Conduire ou lors du retour Préparer.

Invariants : GPS, géocodage, routage, horizon dynamique, géométrie de rotation, ruban bleu et guidage non modifiés.
