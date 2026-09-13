# J240 — Test global JEPALYS

Cette version regroupe en un seul chantier les corrections WP35 et la remise en service du cœur POI, afin d'éviter une succession de micro-patches.

## À tester sur WP35
1. Accueil portrait puis paysage : vignettes, logo, ID véhicule / Mes tournées, carte Itinéraire entièrement visible.
2. Paramètres ⚙ : Auto par défaut ; forçage Jour et Nuit disponible ; revenir sur Auto.
3. Destination classique : Ma position → destination → 3 itinéraires → Conduite.
4. Recherche de lieu : « Carrefour Perpignan » ou un autre magasin + localité ; choisir le résultat puis démarrer.
5. Catégories : aire de repos, aire camping-car, parking, station, GPL, eau/vidange, camping, centre commercial.
6. Conduite portrait : `◎`, `+`, `−` tous visibles et tactiles ; panneau 70 et Arrivée/Reste/Temps corrects.
7. Conduite paysage : GPS et profil non superposés ; trois commandes loupe visibles ; commandes de carte compactes ; panneau de manœuvre contenu.
8. Démo sans GPS : véhicule toujours sur le tracé, pas de reconstruction du tracé à chaque mouvement, surveiller disparition du voile blanc et des oscillations.
9. Vérifier la netteté des textes, pictogrammes, véhicule et fonds Carte / Relief / Satellite.

## Limite volontaire connue
La vue Relief utilise OpenTopoMap raster. Le hachurage des bâtiments est intégré aux images des tuiles : JEPALYS ne peut pas le remplacer proprement par un aplat sans changer de style/fournisseur cartographique. J240 ne maquille donc pas cette couche avec un filtre.


### Clavier prédictif
- Commencer à saisir un mot : vérifier 1 à 3 complétions locales au-dessus du clavier.
- Destination : après au moins 3 caractères et une courte pause, vérifier l’apparition de propositions de lieux réels.
- Toucher une proposition : le texte doit être complété ; pour un lieu réel, ses coordonnées doivent être conservées jusqu’au calcul.
- Vérifier portrait + paysage et confirmer qu’aucun clavier Android ne s’ouvre.
