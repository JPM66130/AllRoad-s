# AllRoad’s — Roadmap

Statuts : **à faire** / **en cours** / **à tester par moi** / **terminée**.

## Phase 0
- **E0 — Documentation projet et état de référence — terminée**
  Créer CAHIER.md, ROADMAP.md, JOURNAL.md, DECISIONS.md et COMMENT-TESTER.md. Faire valider CAHIER + ROADMAP. Ensuite seulement initialiser Git et créer le premier commit sans supprimer les fichiers existants.

## Priorité essais routiers
- **E1 — Stabiliser la base V52.9.95 — terminée**
  Mettre en cohérence version/cache/PWA/lanceur et l’autorité des fichiers frontend sans modifier la coque validée. Vérifier démarrage + tests.
- **E2 — Déplacement de conduite fluide — terminée**
  Remplacer la logique de scène figée comme cible de travail par un mouvement continu performant ; HUD indépendant et stable ; portrait/paysage. Une seule boucle d’animation autoritaire et redimensionnement uniquement sur changement significatif/orientation. Mesurer le comportement réel plutôt que promettre un nombre d’images/seconde.
- **E3 — GPS réel et progression synchronisée — à tester par moi**
  Correctif mouvement réel 2026-09-09 : `syncMobileDriveMarker()` ne prend plus le premier point de l’itinéraire comme position de véhicule. En conduite réelle, le GPS est désormais l’unique autorité de position ; avant le premier fix fiable, aucun marqueur n’est inventé. Chaque fix GPS met à jour le marqueur avant le recentrage caméra.
  Architecture conservée : une seule autorité GPS continue, séparation explicite GPS réel/simulation, vitesse native ou calculée entre deux positions fiables si Android ne fournit pas `coords.speed`, progression sur route, comportement GPS incertain/perdu et retour au signal fiable. Validation dynamique WP35 requise avant E6.
- **E4 — Sortie d’itinéraire et recalcul — à faire**
  Confirmer la déviation avant recalcul ; recalcul automatique selon sécurité/compatibilité/confort/temps-distance.
- **E5 — Alertes essentielles de conduite — terminée**
  Validée sur WP35 en simulation sans GPS : une seule autorité `AllRoadsAlertRuntime`, visuel critique validé, 3 annonces vocales maximum par alerte, rappels géolocalisés 300 m / 100 m / entrée, une annonce unique de fin de zone, priorités centralisées et états périmés nettoyés.
- **E6 — Premier essai routier réel — en attente de E7**
  Essai routier court et contrôlé servant notamment à valider E3 en mouvement réel (vitesse/progression/synchronisation), sans absorber E4. E6 ne démarre qu’après validation de la vue de conduite réelle E7. Les sorties d’itinéraire et recalcul restent exclusivement dans E4.

- Diagnostic HGV : chargeur de clés ORS/GraphHopper rendu compatible avec le nom historique encodé ; validation réelle sur WP35 requise.

## Fonctions V1 après socle routier
- **E7 — Vue de conduite réelle — à tester par moi**
  Brique cartographie/conduite reconstruite : une seule autorité par état. Préparer = Leaflet Europe ; Prêt = Leaflet + itinéraire ; Conduite GPS réelle = Leaflet ; Démo sans GPS = canvas synthétique. Le passage d’une démo à un trajet réel remet explicitement le mode réel, sans conserver l’état de simulation.
  En conduite GPS réelle, la carte/route Leaflet est autoritaire : position véhicule GPS, orientation selon déplacement, progression, caméra/zoom de conduite et HUD existant conservé. Deux cadrages partagent exactement la même navigation : « dans le véhicule » (défaut, véhicule non affiché) et « au-dessus du véhicule » (caméra plus haute/reculée, véhicule visible). Le canvas synthétique E2 reste réservé à la simulation/démo sans GPS. E7 doit être validée avant E6.
- **E8 — STOP Bus et 20 itinéraires — à faire**
  STOP Ramassage/Dépose/Les deux, nom facultatif, GPS, stockage par itinéraire, modification et rappel visuel/vocal.
- **E9 — POI OpenStreetMap dans rayon 10 km — à tester par moi (J240)**
  Catégories V1, compatibilité véhicule, distance routière et impact du détour.
- **E10 — Source POI camping-car spécialisée — à faire**
  Étudier licence, qualité, couverture et coût ; présenter les options avant toute dépense ou intégration payante.
- **E11 — Signalements communautaires — à faire**
  Création/confirmation, regroupement d’événements, confiance, expiration, effet sur alertes et recalcul.
- **E12 — Commandes vocales — à faire**
  Bouton micro, commandes principales, choix vocal des POI, annulation et fonctionnement dégradé.
- **E13 — Activation mains libres « AllRoad’s » — à faire**
  Étudier faisabilité, batterie, confidentialité, Android/iOS et coûts éventuels avant choix technique.
- **E14 — Multilingue européen — à faire**
  Centraliser toutes les chaînes et préparer l’architecture multilingue unique ; définir et intégrer les langues sans dupliquer l’application.
- **E15 — Comptes, droits et garage partagé — à faire**
  Free/abonnements ; Particulier 2 utilisateurs/garage partagé/données personnelles ; Pro 1 utilisateur ; droits serveur.
- **E16 — Robustesse V1 multi-support — à faire**
  Réseau absent, GPS refusé, batterie faible, rotation/redimensionnement, grands volumes de POI, téléphone/tablette/PC.

## Règle de progression
Une seule étape de développement à la fois. À la fin : tests techniques, procédure de test téléphone, statut **à tester par moi**. Après validation utilisateur : **terminée** et un commit Git clair en français.

- **E7 — contrôleur d’état cartographie/conduite — à tester par moi.** Chasse aux fantômes terminée côté code : un seul contrôleur `panel(state)`, transition vers Prêt uniquement après `allroads:route-ready`, cadrages différés annulés à chaque changement d’état, ancien moteur photo/WebGL retiré de la brique. Préparer = Europe Leaflet ; Prêt = tracé Leaflet ; Conduite réelle = Leaflet ; Démo conduite = canvas synthétique.


### E7 — isolation physique carte / démo
- Statut : **à tester par moi**.
- Leaflet et la démo synthétique sont désormais deux surfaces distinctes : la démo ne vit plus dans `#map`.
- En mode démo, la carte entière est désactivée et un canvas plein écran dédié prend le relais ; en Préparer/Ready/Réel, cette surface démo est absente.
- Objectif du test WP35 : vérifier disparition de la couche bleue partielle et observer si ce découplage supprime aussi le fantôme de Préparer.

### E7 — Préparer : couche cartographique isolée
- Statut : **à tester par moi**.
- Démo, Prêt et Conduite réelle sont conservés tels que validés au dernier test.
- Préparer utilise une couche Leaflet fraîche et indépendante, supprimée dès la sortie de l'état.

### E7 — Préparer remis à nu
- Statut : **à tester par moi**.
- Préparer ne réutilise plus `#map` : nouvelle surface + nouvelle instance Leaflet dédiées à la carte Europe.
- Prêt, Conduite réelle et Démo restent gelés sur le fonctionnement déjà validé.


### E7 — réparation de chaîne hors navigation
- Statut : **à tester par moi**.
- La surface Préparer dédiée ne peut plus exister visuellement sur Accueil / choix profil / fiche véhicule.
- Objectif immédiat : vérifier Accueil → Bus → véhicule → Continuer vers l’itinéraire, puis seulement reprendre le diagnostic de la carte Europe de Préparer.


### E7 — retour propre vers Préparer
- Statut : **à tester par moi**.
- Retour depuis Itinéraire prêt et action Modifier utilisent désormais le même nettoyage complet avant de réafficher Préparer.
- Aucun changement fonctionnel de Prêt, Conduite réelle ou Démo.
- Test décisif : Accueil → Bus → véhicule → Préparer → Itinéraire prêt → Retour → Préparer ; la carte Europe doit être seule, sans photo, voile, route ni résidu de conduite.

- E7 — Décapage historique Préparer : **à tester par moi**. Anciennes couches V52.8.x neutralisées dans Préparer/Ready ; ordre d'ouverture V52.9.95 restauré ; 272 tests automatisés OK.

- [À TESTER WP35] E7 — caméra GPS conducteur réelle : cap en haut, véhicule vers le bas, route à venir prioritaire, zoom adapté à la vitesse.

## 2026-09-10 — Raccord saisie trajet → géocodage réel
- Correction prioritaire avant essai route : l'écran mobile géocode désormais le départ ET la destination visibles avant tout calcul.
- Les anciennes coordonnées Ille-sur-Têt / Vinça ne peuvent plus être réutilisées silencieusement pour un trajet saisi différent.
- « Ma position » utilise une position GPS réelle (position connue ou acquisition ponctuelle), jamais les coordonnées de démonstration.
- Aucun changement de caméra, E5, Préparer/Prêt ou moteur de routage.
- Tests automatiques : 280 réussis. Statut : à tester par Jean-Paul sur WP35.

- [À TESTER] Géocodage universel : résolution séquentielle départ → destination avec biais de proximité pour les noms ambigus (Vinça, Bages, etc.).

### E7 — Géocodage universel / homonymes — À TESTER
- [x] Départ et destination visibles géocodés avant calcul.
- [x] Focus géographique transmis au géocodeur.
- [x] Reclassement AllRoad’s des homonymes par proximité du départ (ne plus faire confiance à l’ordre fournisseur).
- [ ] Validation WP35 : Vinça, Thuir, Le Boulou, Bages.
- **Géocodage avant E6 — à tester par moi (2026-09-10)** : « Ma position » ne peut plus provenir d'un marqueur Leaflet de démo/ancien trajet ; elle exige une mesure GPS navigateur fraîche. Cette position réelle sert ensuite de focus au classement des homonymes de destination.
\n- [À TESTER WP35] Géocodage : blocage de chargement identifié dans le lanceur ; URL de build renouvelée (`geofresh1`) pour empêcher la réutilisation silencieuse de l’ancienne page. Tester une destination différente avant toute nouvelle correction métier.\n
- [À TESTER WP35] Diagnostic géocodage `geodiag1` : aucune nouvelle règle métier ; afficher les coordonnées départ/destination sélectionnées et celles réellement envoyées au routeur. Une capture d'écran doit suffire à identifier la brique fautive.
- [À TESTER WP35] Diagnostic GPS source : afficher précision + heure de la mesure fraîche utilisée par « Ma position » ; géocodage destination gelé pendant ce diagnostic.

- **E3 — consolidation source « Ma position » — à tester par moi (2026-09-10).** Le départ de préparation utilise désormais `AllRoadsGpsRuntime.requestFreshPosition()` et le même `watchPosition` centralisé que la conduite ; aucun marqueur Leaflet ni `getCurrentPosition()` indépendant dans cette chaîne. Fix requis avec précision <= 50 m. Test WP35 immédiat : Ma position → Thuir.

- **E3 — règle définitive « Ma position » — à tester par moi (2026-09-10).** Recherche GPS haute précision démarrée dès Préparer ; position jamais anticipée. Fix frais <= 15 s et précision <= 50 m obligatoire avant tout calcul depuis « Ma position ». En absence de fix : « Recherche de votre position GPS… », sans position de secours.

- [À TESTER WP35] Géocodage intermittent : une panne ORS/Pelias n’est plus confondue avec « adresse introuvable » ; un second essai est effectué avant erreur temporaire explicite. GPS inchangé.
