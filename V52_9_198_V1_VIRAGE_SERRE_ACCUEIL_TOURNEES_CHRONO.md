# V52.9.198 — V1 « Virage Serré »

## État des lieux correctif
- Suppression des autorités clavier concurrentes V181, V183, V185, V186, V195, V196 et V197.
- Une seule autorité de saisie V198.
- Une seule autorité de menus Virage Serré V198.

## Corrections Accueil
- Barre de saisie JEPALYS visible au-dessus du clavier Android.
- Repositionnement portrait/paysage avec VisualViewport.
- Menus ID véhicule et Mes tournées accessibles et recalculés après rotation.
- Cadre maître stable des vignettes profils.
- Modifier manuellement Destination désactive automatiquement la tournée active.

## Tournées Bus
- Charger une tournée restaure ses données sauvegardées et remplit l’itinéraire.
- Bouton Retour : inverse départ/destination et inverse aussi stops/route si ces données existent.
- Le schéma de tournée conserve les champs stops et route pour l’extension arrêt par arrêt.

## Conduite Bus
- Chronomètre visible uniquement en profil Bus.
- Arrêt confirmé après 3 s sous 0,8 km/h.
- Au redémarrage à partir de 2 km/h : départ du chronomètre à 00:00.
- Reset à chaque nouvel arrêt confirmé.
- API interne prête pour l’écart horaire : vert < +3 min, orange dès +3 min de retard ou -5 min d’avance, seuil +5 min renforcé.

Aucun changement du GPS, du routage, du moteur cartographique ou de l’autorité caméra.
