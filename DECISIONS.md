# AllRoad’s — Décisions durables

1. **Conserver la technologie actuelle.** La base V52.9.95 fonctionne et ses 220 tests passent ; aucune réécriture ni changement de technologie sans accord explicite.
2. **Une seule application responsive.** Android, iPhone, tablette et PC ; adaptation automatique et déterministe. ADN : « Partout, pour tous ! ».
3. **8 profils visibles.** Piéton, Vélo, Moto, Voiture, Utilitaire, Camping-car, Bus, Poids lourd.
4. **Sécurité de routage :** compatible d’abord, optimal ensuite. Classement : sécurité → compatibilité → confort véhicule → temps/distance.
5. **GPS :** continuité estimée seulement tant qu’elle reste crédible ; jamais de fausse précision.
6. **Recalcul :** confirmer une vraie sortie de route avant recalcul automatique.
7. **Demi-tour/blocage :** ne jamais traverser la zone bloquée/dangereuse pour rejoindre une solution proposée.
8. **Alertes :** visuel + vocal, priorité critique → sécurité → navigation → information/confort, sans chevauchement vocal ni saturation.
9. **POI V1 :** OSM + seconde source camping-car à sélectionner après étude licence/qualité/coût ; rayon de proposition maximal 10 km autour du trajet, puis classement par détour réel.
10. **Communauté :** conserver source/date/confiance ; regroupement automatique du même événement ; expiration/reconfirmation ; un vote communautaire ne transforme jamais une interdiction officielle en route compatible.
11. **Voix :** bouton + mains libres « AllRoad’s » si autorisé ; commandes claires exécutées directement ; choix utilisateur requis pour changer de destination POI ; annulation immédiate des actions annulables.
12. **Bus :** STOP métier propre aux 20 itinéraires enregistrés ; Ramassage/Dépose/Les deux, GPS, nom facultatif, rappel visuel/vocal et édition ultérieure.
13. **Commercial :** Free permanent limité + payant. Particulier = 2 utilisateurs et garage partagé ; Pro = 1 utilisateur. Trajets/favoris/historique/préférences personnels.
14. **Multilingue européen V1 :** système centralisé dans la même application, pas une application par langue.
15. **Hors-ligne V1 :** continuité temporaire du trajet déjà chargé, pas de cartographie hors ligne complète.
16. **Priorité immédiate :** mouvement/fluidité, GPS et guidage réel avant recherche de photoréalisme ; puis alertes.
17. **Coûts :** aucune API, clé, licence, serveur ou service payant engagé sans avertissement préalable avec estimation et validation.
18. **Données/secrets :** aucun secret dans le code partagé ; aucun fichier/donnée supprimé sans accord.

## D-2026-09-09 — Convention de nommage du lanceur
À partir de la base validée E1, le lanceur principal commence par `AA_` (ex. `AA_LANCER_ALLROADS_V52_9_95.bat`) afin d’être immédiatement visible en haut du dossier sous Windows.

## V52.9.129 — rotation cartographique
- Toute couverture supplémentaire nécessaire après rotation doit être calculée à partir de la géométrie réelle du viewport et de l'angle de rotation.
- Interdiction de réintroduire un `scale(...)` constant non compensé dans la caméra.


## V52.9.181
Clavier Android intégré aux formulaires : pas de barre flottante doublon, validation par touche Entrée/✓, identification véhicule persistée et répercutée immédiatement sur l’accueil.

- V52.9.182 — Barres Android : elles font partie du cadre d’usage. JEPALYS doit rester stable avec les barres système visibles et dimensionner sa coque sur la zone utile, sans dépendre d’un mode immersif/fullscreen.

## V52.9.182 — Accueil conditionné au profil
Le bloc « Mon véhicule sélectionné » n’est pas affiché pour Piéton, Vélo et Moto. Deux compositions d’accueil sont maintenues et harmonisées dans les deux orientations ; l’absence du bloc ne doit jamais laisser un espace vide.

## V52.9.188 — branche « virage-serre »
- Expérimenter une architecture visible à **deux vues seulement : Accueil + Conduite**.
- Ne pas réécrire les moteurs GPS, routage ou conduite : les appeler depuis le nouvel accueil.
- Remplacer la page véhicule dédiée par des commandes compactes sur l'accueil et des fenêtres flottantes.
- « Mon véhicule » : ajouter, identifier, modifier les caractéristiques, sauvegarder.
- « Mes tournées » : créer, charger et gérer les tournées depuis l'accueil.
- L'itinéraire est préparé depuis l'accueil ; la conduite reste la vue métier existante.


## V52.9.195 — Virage serré — finition saisie
Option A clavier validée : clavier Android natif conservé, saisie JEPALYS flottante au-dessus du clavier, menus paysage sur hauteur utile, doublon Tournée supprimé.

## V198 — stabilité saisie et chrono Bus
- La barre JEPALYS de saisie doit rester visible dans la partie haute du viewport pendant l'ouverture du clavier, notamment en paysage.
- En paysage, les menus métier utilisent la partie droite disponible et sont recalculés lors d'un vrai changement d'orientation.
- Le chronomètre Bus est placé sur le côté droit, juste au-dessus du bouton ARRÊT.

## Audit correctif V198 — focus natif + barres Android
- Réservation artificielle V184 neutralisée : JEPALYS utilise désormais uniquement le viewport réellement fourni par Android/Chrome, pour supprimer les grandes bandes noires.
- Saisie simplifiée : le champ réellement touché devient lui-même la zone de saisie flottante. Il reçoit directement le focus issu du geste utilisateur ; aucun second champ ne remplace le focus Android.
- Destination manuelle : désactivation de la tournée active maintenue au premier toucher.
- Menus ID/Tournées conservés, repositionnés après rotation.
- Chronomètre Bus inchangé dans cet audit.

## V52.9.199 — V1 « Virage Serré » — autorité 2 vues
- Le flux visible est limité à Accueil et Conduite.
- Les vues legacy Sélection véhicule / Préparer le trajet / Itinéraire prêt restent internes au moteur et ne doivent jamais être affichées.
- Depuis Conduite, un seul bouton de navigation principal reste visible : Accueil.
- La saisie active est l'autorité visuelle temporaire absolue : le vrai champ HTML passe au premier plan, sans clone.
- Destination appelée pour modification : ancienne valeur remplacée, tournée active désactivée.
- Une tournée chargée est l'autorité de son trajet sauvegardé ; le bandeau affiche le sens actif départ → destination.
- « Retour » inverse départ/destination et l'ordre des arrêts sauvegardés.
- Les vignettes profils sont centrées. Les encarts promotionnels ne peuvent jamais recouvrir les fonctions métier.

## V52.9.200 — règle deux vues propre
- Avant correction : nettoyage obligatoire des autorités concurrentes ; aucune rustine additionnelle.
- Deux vues visibles seulement : Accueil et Conduite.
- Sélection véhicule, Préparer le trajet et Itinéraire prêt sont legacy et ne doivent jamais devenir visibles/interactifs.
- Démarrer calcule en arrière-plan sur l’Accueil puis bascule directement en Conduite.
- Tournée active = autorité d’affichage du trajet ; bandeau et Itinéraire montrent le même départ - destination ; Retour inverse les deux.

## V52.9.201 — architecture 2 vues
Les seules vues visibles de V1 Virage Serré sont Accueil et Conduite. Les pages legacy Sélection véhicule, Préparer le trajet et Itinéraire prêt sont supprimées du DOM. Le moteur peut conserver temporairement des champs cachés d’adaptation, sans UI ni navigation.

## Règles figées — V52.9.202
- Une seule chaîne de routage visible : Accueil → calcul silencieux → Conduite. Aucune page intermédiaire.
- « Ma position » n’utilise qu’un fix GPS frais et fiable provenant de l’autorité GPS ; aucune position inventée ou ancienne.
- L’Accueil anticipe la recherche GPS pour réduire l’attente au clic sur Démarrer.
- Une erreur de géocodage ou de routage maintient l’utilisateur sur l’Accueil avec message clair.
- En saisie métier, le vrai champ HTML reste au premier plan ; fenêtre légèrement remontée/compactée, sans clone ni rustine de viewport.

## Décision UI — panneaux métier Accueil
Les panneaux `ID véhicule` et `Mes tournées` doivent partager le même ancrage visuel : ouverture dans l'axe de leur rangée, avec le haut du panneau positionné approximativement au milieu des boutons d'appel. En saisie, la fenêtre métier reste l'autorité et se place suffisamment haut pour garder le vrai champ visible au-dessus du clavier.

- Saisie Accueil : les panneaux ID véhicule / Mes tournées chevauchent la moitié basse de leurs boutons d’appel ; le bloc Itinéraire actif passe au premier plan au-dessus du clavier.

- Saisie Accueil : la touche Entrée/Validation du clavier valide le formulaire actif. Les panneaux ID/Tournées s’ancrent à la moitié exacte de la hauteur de leur bouton d’appel.

## Règles figées — V52.9.206
- Une saisie importante possède toujours un bouton de validation visible ; Entrée déclenche la même action.
- Un panneau déroulant ne doit jamais rendre son bouton d’appel inaccessible.
- Piéton = itinéraire uniquement ; Vélo/Moto = fonctions pro légères ; profils routiers = gestion complète.


## Décision V207 — autorité de saisie
Tous les champs JEPALYS utilisent le clavier intégré plein écran ; le clavier Android est neutralisé. × annule, Valider applique.
