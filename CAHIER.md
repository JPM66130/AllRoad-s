# AllRoad’s — Cahier V1

## ADN produit
**« Partout, pour tous ! »**

AllRoad’s est une application unique de navigation routière adaptative, utilisable sur téléphone, tablette et PC, en portrait ou paysage. L’interface s’adapte automatiquement au support et à l’espace disponible sans modifier arbitrairement la composition validée.

## Utilisateurs et profils
Les 8 profils restent visibles : Piéton, Vélo, Moto, Voiture, Utilitaire, Camping-car, Bus, Poids lourd. Au lancement, Voiture et Bus peuvent être débloqués en priorité ; les autres restent visibles mais verrouillables selon les droits.

## V1 indispensable
- Navigation GPS en temps réel avec progression sur l’itinéraire et recalcul automatique après confirmation d’une vraie sortie de route.
- Profil véhicule complet : hauteur, poids, longueur, largeur, GPL, matières dangereuses et contraintes particulières.
- Compatibilité véhicule prioritaire : **compatible d’abord, optimal ensuite**.
- Classement des itinéraires : sécurité → compatibilité → confort adapté au véhicule → temps/distance.
- Préférence conducteur : Prudent / Équilibré / Rapide, avec Équilibré par défaut ; jamais de contournement d’une règle de sécurité.
- 2 ou 3 itinéraires compatibles avant le départ, meilleur choix clairement mis en avant.
- Alertes de sécurité visuelles et vocales, hiérarchisées et anti-saturation.
- POI camping-car intelligents.
- Multilingue européen dès la V1 avec système de traduction centralisé dans une seule application.
- Défilement de conduite fluide et HUD stable/lisible.

## GPS et continuité
En perte GPS courte, AllRoad’s peut estimer brièvement la progression à partir de la dernière position fiable, de l’itinéraire et du mouvement, avec indication claire « GPS incertain ». Au retour du signal, le recentrage est progressif. Si l’incertitude devient trop grande ou trop longue, l’estimation s’arrête : l’itinéraire et la dernière position fiable restent affichés et l’utilisateur est informé que la position GPS est indisponible.

## Réseau / hors connexion V1
Pas de cartographie hors ligne complète en V1. Un trajet déjà chargé doit cependant pouvoir continuer lors d’une perte réseau temporaire dans la mesure des données déjà disponibles.

## Sécurité et recalcul
Une incompatibilité certaine (gabarit, poids, largeur, GPL, interdiction…) entraîne le rejet automatique de l’itinéraire et le calcul d’une solution compatible, avec explication. Une donnée incertaine génère un risque à vérifier et ne devient pas arbitrairement une interdiction certaine.

Lors d’un obstacle ou blocage : chercher d’abord une solution sûre accessible sans traverser la zone dangereuse ; sinon chercher une zone de retournement compatible avant le blocage. Ne jamais proposer une manœuvre imposant de traverser la zone bloquée/dangereuse.

## Alertes
- Visuel + vocal + niveau de priorité selon le danger.
- Première alerte critique complète ; rappels suivants courts et uniquement au moment pertinent.
- Arrêt des rappels lorsque la solution est suivie ou que le danger s’éloigne.
- Une seule annonce vocale à la fois : critique → sécurité → navigation → information/confort.
- Un danger communautaire n’impose un recalcul automatique que s’il est suffisamment crédible et réellement dangereux/incompatible pour le véhicule.

## POI
Catégories V1 : aires camping-car, eau/vidange, stations GPL, parkings adaptés, campings.

Sources : OpenStreetMap + une seconde source spécialisée camping-car à sélectionner après vérification de sa licence, de sa qualité et de son coût. Aucun service payant ne sera engagé sans validation préalable.

AllRoad’s peut proposer proactivement des POI sur le trajet ou dans une zone maximale de 10 km autour de celui-ci, puis les classer selon pertinence et détour routier réel. Afficher distance routière et impact du détour (ex. +6 min). Les préférences POI sont personnelles à chaque utilisateur.

## Communauté
Les utilisateurs peuvent signaler fermetures, services en panne, accès incompatibles, travaux, dangers et erreurs de données. Un signalement communautaire ne remplace pas immédiatement la source officielle. Sa fiabilité tient compte notamment de sa date, de sa source et des confirmations.

Les signalements correspondant au même événement (zone/type/période cohérents) sont regroupés automatiquement en un événement unique dont la confiance évolue. Les événements proches mais différents ne doivent pas être fusionnés. Les dangers temporaires expirent et peuvent être reconfirmés par les conducteurs passant à proximité via une demande légère « Danger toujours présent ? Oui / Non ».

## Voix
- Signalement par bouton et par voix.
- Bouton micro + activation mains libres « AllRoad’s » si l’utilisateur l’autorise ; désactivable.
- Commandes principales de conduite : signaler, chercher une aire, station GPL, parking, retour, etc.
- Commande claire : exécution directe ; confirmation uniquement si ambiguë, importante ou risquée.
- Pour plusieurs POI : annoncer les 2 ou 3 meilleurs, meilleur en premier, puis choix conducteur.
- Sans réponse : aucune modification automatique du trajet.
- « AllRoad’s, annule » annule immédiatement la dernière action/proposition encore annulable, sans compromettre une action de sécurité.
- L’application reste utilisable si la reconnaissance vocale est indisponible.

## Mode Bus — STOP métier
Le profil Bus possède un bouton STOP dédié. Pendant un trajet, un appui propose : **Ramassage / Dépose / Les deux**. Le STOP mémorise sa position GPS et peut recevoir un nom facultatif saisi ou dicté.

Chaque STOP est rattaché à l’un des **20 itinéraires Bus enregistrés** et est retrouvé lors des utilisations ultérieures de cette ligne. À l’approche, AllRoad’s avertit automatiquement visuellement et vocalement en utilisant, si disponibles, le nom et le type (ex. « Dans 300 mètres, arrêt Mairie — ramassage »). La distance exacte sera réglée par les essais routiers.

Les STOP d’un itinéraire peuvent ensuite être modifiés : nom, type, position ou suppression. Ces arrêts métier restent distincts des POI généraux.

## Comptes et offre
Modèle : Free permanent limité + abonnements/fonctions avancées.
- Particulier : 1 abonnement = 2 utilisateurs distincts.
- Pro : 1 abonnement = 1 utilisateur.
- Particulier : garage/véhicules partagés entre les 2 utilisateurs ; trajets, favoris, historique et préférences POI personnels.
- Un véhicule partagé possède une fiche canonique unique ; les deux utilisateurs peuvent la modifier.

## Supports
Android + iPhone + tablette + PC avec une seule application responsive. Adaptation automatique et déterministe : uniquement sur vrai changement de viewport/orientation ou redimensionnement, jamais à cause d’un geste accidentel.

## Hors périmètre V1
- Cartographie hors ligne complète téléchargeable.
- Multiplication d’applications distinctes selon support, langue ou client.
- Réalisme visuel photoréaliste fixe comme objectif prioritaire : le mouvement, la fluidité, le GPS et la sécurité passent avant.

## Objectif immédiat
Préparer les premiers essais routiers réels : mouvement fluide, GPS réel, guidage synchronisé, puis alertes essentielles, sans casser la coque WP35 validée.
