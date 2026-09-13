# AllRoad’s — Journal de développement

## 2026-09-09 — Phase 0 / audit et cadrage
### Fait
- Lecture et audit de la base V52.9.95.
- Application identifiée : FastAPI/Python + HTML/CSS/JavaScript + Leaflet + base locale SQLite.
- Démarrage vérifié : `/`, `/version` et `/app/` répondent correctement.
- Suite de tests vérifiée : **220 tests réussis**.
- Les trois fichiers cœur frontend sont actuellement identiques entre `frontend/` et `api/frontend/`.
- Recueil du besoin V1 : profils, véhicule, navigation, GPS, sécurité, POI, communauté, voix, abonnements, multi-support et STOP Bus.
- Création des cinq fichiers de mémoire projet imposés.

### Reste à faire
- Faire valider `CAHIER.md` et `ROADMAP.md` par le client.
- Après validation seulement : initialiser Git et créer le premier commit.
- Commencer ensuite E1, puis priorité aux essais routiers : fluidité → GPS → recalcul → alertes.

### Points techniques constatés
- Des références de version/cache PWA sont encore anciennes par rapport à V52.9.95.
- `ARCHITECTURE_ALLROADS.txt` et l’état réel des deux frontends ne sont pas parfaitement cohérents.
- Les dépendances Python ne sont pas figées par version.
- Le projet contient des environnements virtuels volumineux ; ils ne seront pas supprimés sans accord.
- Git n’est pas encore initialisé dans cette copie.

### Décisions
Voir `DECISIONS.md`. Aucun code applicatif n’a été modifié pendant cette étape documentaire.


## 2026-09-09 — E1 / Stabilisation V52.9.95
### Fait
- CAHIER.md et ROADMAP.md validés par le client.
- Git initialisé et premier point de référence créé.
- Version PWA, manifeste, service worker et lanceur WP35 alignés sur V52.9.95.
- Autorité frontend clarifiée : FastAPI sert `api/frontend/`; `frontend/` reste un miroir de compatibilité tant que les tests historiques l'exigent.
- Aucun fichier existant supprimé.

### À tester par moi
- Lancer WP35 avec le lanceur V52.9.95.
- Vérifier que l'accueil s'ouvre normalement et affiche V52.9.95.
- Passer Accueil -> Préparer le trajet -> Afficher l'itinéraire -> Conduite et vérifier que la coque validée n'a pas changé.

### Suite
- Après validation client : marquer E1 terminée et créer son commit Git.
- Puis E2 : déplacement de conduite fluide.

- 2026-09-09 — E1 correction paysage véhicule : prise en compte explicite du bloc Identification dans la grille ; portrait inchangé ; 220 tests OK. Statut : à tester par moi.

- 2026-09-09 — E1 correction saisie trajet + paysage véhicule : panneau de saisie maintenu visible au-dessus du clavier en paysage, suppression du fond noir de préparation, grille véhicule corrigée sur 7 zones réelles ; 220 tests OK. Statut : à tester par moi.


## 2026-09-09 — E1 nettoyage responsive avant nouveau correctif
- Diagnostic confirmé : plusieurs règles historiques de coque/clavier se contredisaient.
- Suppression des deux rustines E1 temporaires et de l’ancien contrôleur clavier V52.9.51.
- Une seule autorité de saisie trajet est désormais placée dans allroads_ui_final.js/css.
- La fiche véhicule paysage utilise explicitement 7 lignes, dont l’identification injectée par JS.
- Portrait conservé tel que validé ; E1 reste à tester par Jean-Paul avant commit.
- À conserver pour la suite : bouton ARRÊT/STOP en mode Bus, lié aux 20 itinéraires enregistrés.

## 2026-09-09 — E1 : nettoyage clavier portrait/paysage (à tester)
- Constat utilisateur : paysage OK pour la saisie, mais en portrait une ancienne hauteur paysage pouvait rester active sous clavier et laisser une bande noire.
- Correction ciblée : une seule règle clavier temporaire utilise `visualViewport` pour la hauteur réellement visible, identique en portrait et paysage.
- La coque normale reste figée hors saisie ; aucune modification du design portrait validé.
- E1 reste **à tester par moi** avant commit.

## 2026-09-09 — E1 : fermeture clavier généralisée (à tester)
- Le comportement de fermeture est maintenant commun à toutes les vues utilisant un champ texte/nombre/mot de passe/textarea, pas seulement au trajet.
- Entrée sur un champ simple ferme le clavier ; un appui sur une action (bouton/lien/commande) retire d'abord le focus et tente de masquer le clavier Android.
- Le positionnement spécial de la feuille de trajet reste limité aux champs Départ/Arrivée ; les autres formulaires conservent leur mise en page et utilisent seulement la visibilité/fermeture commune.
- Aucun changement de design ; E1 reste **à tester par moi** avant commit.

## 2026-09-09 — E1 : visibilité globale des champs sous clavier (à tester)
- Retour utilisateur : la saisie Trajet fonctionne désormais, mais le champ Identification véhicule reste hors zone visible, surtout en paysage.
- Cause : le contrôleur commun mesurait `visualViewport` uniquement pour les champs Départ/Arrivée ; les autres vues ne recevaient pas la hauteur réellement visible avant `scrollIntoView`.
- Correction ciblée : la mesure du clavier est maintenant calculée pour tous les champs éditables ; la page Véhicule devient temporairement scrollable pendant la saisie afin d'amener le champ actif au-dessus du clavier.
- Hors saisie, la composition portrait/paysage reste inchangée. E1 reste **à tester par moi**.

## 2026-09-09 — E1 : barre de saisie AllRoad's + nettoyage conflits clavier (à tester)
- Décision produit : toutes les saisies doivent afficher une barre AllRoad's stable en haut, sur le modèle de Préparer le trajet, sans dépendre de la barre Android.
- Suppression du redimensionnement/défilement temporaire spécifique à la page Véhicule, source d'instabilité sous clavier.
- Les champs hors trajet conservent désormais la coque normale ; la barre AllRoad's reflète en direct le champ actif et propose une validation ✓ qui ferme le clavier.
- Préparer le trajet conserve sa logique déjà validée ; aucune nouvelle règle de déplacement n'a été ajoutée à la page Véhicule.
- E1 reste **à tester par moi** avant tout commit.


- E1 : suppression de la zone sombre résiduelle sous la vue Véhicule pendant la saisie clavier, en reprenant le principe visuel stable de Prépa trajet.

## 2026-09-09 — E1 validée
- Validation utilisateur obtenue après test WP35 portrait/paysage et saisie clavier.
- Barre de saisie AllRoad’s visible et stable ; disparition de la zone noire résiduelle validée.
- E1 passe à **terminée**.
- Convention adoptée pour la suite : le lanceur commence par `AA_` afin d’apparaître en haut du dossier.
- Aucun passage à E2 avant ce commit de référence.


## 2026-09-09 — E2 déplacement de conduite fluide (à tester)
- La scène photo figée n'est plus l'autorité visuelle en conduite : le moteur animé reprend l'affichage en portrait et paysage.
- Le moteur n'est plus bridé artificiellement à 24 i/s : rendu piloté directement par `requestAnimationFrame` avec déplacement calculé au temps réel, sans promettre une fréquence fixe.
- Le HUD reste indépendant du canvas de mouvement et n'est pas animé par E2.
- Un compteur interne `window.AllRoadsDriveMotionStats` mesure la fréquence réellement observée, les dimensions et l'état du moteur pour le diagnostic, sans encombrer l'interface conducteur.
- Les anciennes scènes photo restent présentes dans les fichiers mais ne peuvent plus masquer le moteur animé. Aucun fichier supprimé.
- E2 reste **à tester par moi** avant commit.

## 2026-09-09 — E2 nettoyage moteur paysage (à tester)
- Retour WP35 : portrait fluide ; changement d'orientation propre ; en paysage, quelques lags et une légère instabilité pendant la conduite.
- Nettoyage ciblé sans modification du design : l'ancien moteur 3D ne lance plus sa boucle `requestAnimationFrame` lorsque le moteur E2 est présent.
- Le canvas E2 n'est plus redimensionné à chaque micro-`resize` Android/WP35 : il attend une variation significative ou un vrai changement d'orientation, avec temporisation courte.
- Une seule boucle d'animation reste autoritaire pour le décor E2 ; le HUD reste indépendant.
- E2 reste **à tester par moi** avant commit.


## 2026-09-09 — E2 validée avec porte de correction
- Validation utilisateur après essai WP35 : portrait fluide et stable ; paysage sans lag ni instabilité remarqués ; changement d’orientation propre.
- E2 passe à **terminée** et devient la nouvelle base de référence pour la conduite animée.
- Principe conservé : cette validation ne fige pas les défauts futurs ; si un problème E2 réapparaît en usage réel, il sera corrigé de façon ciblée sans remettre en cause la base propre et stable.
- Clôture technique : tests et contrôles de l’archive E2 déjà passés avant validation utilisateur ; commit E2 effectué après validation.


## 2026-09-09 — E3 GPS réel, première passe à tester
- E3 passée en `à tester par moi`.
- Le mouvement de la scène de conduite est maintenant asservi à la vitesse GPS réelle : à l’arrêt le décor s’arrête, en mouvement il progresse selon la vitesse reçue.
- Une position GPS de précision <= 50 m devient la dernière position fiable ; une mesure moins précise affiche `GPS INCERTAIN` et conserve la dernière position fiable au lieu de faire sauter le guidage.
- Après 15 s sans nouvelle mesure, l’état devient `GPS INDISPONIBLE`, le déplacement visuel s’arrête et la dernière position/route fiable reste affichée.
- Au retour d’une position fiable, le guidage reprend sans effacer l’itinéraire.
- Aucun recalcul de sortie d’itinéraire n’est ajouté ici : il reste du ressort de E4.

## 2026-09-09 — E3 audit puis nettoyage architectural GPS (à tester)
- Essai utilisateur interrompu : compteur resté à 0 km/h et doute légitime sur l’utilisation du GPS réel.
- Audit avant correction : le projet contenait encore un chemin historique de simulation capable d’écrire des vitesses, tandis que la conduite mobile devait devenir explicitement GPS réel.
- Nettoyage effectué : une seule souscription `watchPosition` reste autoritaire pour le GPS réel ; le mode normal et la simulation sont isolés et ne peuvent plus se substituer silencieusement l’un à l’autre.
- L’état de démarrage affiche désormais `GPS EN ATTENTE` avec vitesse `--` tant qu’aucune vitesse réelle exploitable n’est disponible ; GPS perdu = pas de mouvement inventé.
- Correctif Android propre : si `coords.speed` n’est pas fourni par le navigateur, la vitesse est calculée entre deux positions GPS fiables successives, avec filtre anti-jitter et plafond de sécurité.
- Les écritures de vitesse de simulation passent par une autorité identifiée séparée ; l’ancien scénario automatique reste interdit en conduite réelle.
- Les fichiers de clés ORS/GraphHopper n’ont pas été modifiés ni déplacés ; ils restent ignorés par Git.
- Contrôles : 228 tests OK, 20 scripts JavaScript valides, un seul `watchPosition`, miroirs frontend identiques.
- E3 reste **à tester par moi** ; aucun commit E3 avant validation WP35.

- E3 : ajout d’un indicateur visible de réception GPS (attente / faible / moyen / bon / indisponible) et maintien du démarrage en conduite avant le premier fix GPS. Le lanceur utilise un identifiant de build E3 pour éviter toute ambiguïté avec une ancienne page chargée.

### 2026-09-09 — E3 — indicateur GPS rendu immédiatement identifiable
- Retour WP35 : l'ancien badge `GPS ···` était techniquement visible mais trop discret pour être identifié comme indicateur de réception.
- Remplacement par un indicateur dédié `SIGNAL GPS` avec pictogramme, 4 barres de niveau et état textuel (RECHERCHE / précision ±m / INDISPONIBLE).
- Même emplacement central en portrait et paysage ; aucune nouvelle logique responsive concurrente.
- La source reste l'unique chaîne GPS E3 existante : l'indicateur ne crée aucun second observateur GPS.
- Vérification : 232 tests réussis, miroirs frontend identiques, un seul `navigator.geolocation.watchPosition`.
- E3 reste à tester par Jean-Paul ; diagnostic HGV volontairement reporté après validation visuelle de l'indicateur.

## 2026-09-09 — E3 diagnostic routage HGV après validation indicateur GPS
- Indicateur GPS en barre haute validé visuellement par le client en portrait/paysage.
- Diagnostic du blocage Bus : la sécurité HGV est cohérente, mais les clés ORS/GraphHopper n’étaient pas chargées car le fichier historique est nommé `cl#U00e9.env` alors que le code cherchait uniquement `clé.env`.
- Correction propre : chargeur de secrets centralisé, variables d’environnement prioritaires, compatibilité avec les deux noms historiques sans renommer ni supprimer le fichier de clés.
- Les valeurs secrètes restent hors Git et ne sont pas recopiées dans la documentation.
- Vérification locale : ORS et GraphHopper sont maintenant détectés comme configurés. L’environnement de test n’a pas de résolution DNS externe, donc le calcul HGV réel doit être confirmé sur WP35 connecté.
- Tests : 234/234 réussis.
- E3 reste à tester : confirmer qu’un itinéraire Bus obtient un calcul HGV vérifié et autorise ensuite la Conduite GPS réelle.

### 2026-09-09 — E3 diagnostic GPS navigateur
- Après autorisation Android en position exacte, le téléphone réel reste sur GPS indisponible, y compris dehors.
- Avant toute correction de comportement, ajout d'un diagnostic passif sur l'unique chaîne `watchPosition` existante.
- L'indicateur de barre haute affiche désormais le code navigateur : E1 AUTORISATION, E2 POSITION, E3 DÉLAI ; le détail complet est aussi publié dans l'état de conduite.
- Aucune simulation ajoutée, aucun second abonnement GPS, aucune modification des clés ORS/GraphHopper.
- E3 reste en cours / à diagnostiquer sur téléphone réel.

- E3 GPS — premier fix : suppression du faux délai de 10 s. Le suivi reste en RECHERCHE sans mouvement inventé jusqu’au premier fix ; le watchdog de perte ne démarre qu’après une première position reçue. Codes d’erreur réels 1/2 restent bloquants. Tests : 235/235.


## 2026-09-09 — E5 priorité des alertes — à tester
- Mise en place d’une seule autorité `AllRoadsAlertRuntime` pour arbitrer les alertes de conduite sans modifier la chaîne GPS E3.
- Priorité appliquée : danger critique > sécurité véhicule/GPS > navigation > information.
- Les restrictions et alertes route existantes passent désormais par cette autorité ; une alerte résolue laisse automatiquement la place à la suivante.
- Vocal critique : message complet à la première apparition, rappel court ensuite ; anti-saturation de 12 secondes et interruption des messages moins prioritaires déjà assurée par le moteur vocal existant.
- Le virage dangereux de la simulation Bus utilise aussi cette même autorité afin de permettre un test WP35 reproductible sans rouler.
- Contrôles : 239 tests réussis, scripts JavaScript valides, miroirs frontend identiques. E5 passe à **à tester par moi** ; aucun commit avant validation utilisateur.


## 2026-09-09 — E5 audit complet après essai WP35
- Retour WP35 : la simulation et le contrôle de vitesse fonctionnent, mais aucune alerte E5 visible n’a été observée. E5 repasse à **en cours**.
- Audit sans correction fonctionnelle : le scénario long qui déclenche `Virage dangereux` ne démarre que pour Bus + trajet Villefranche/Vernet, alors que la démo générale peut rouler sans satisfaire cette condition ; l’événement est en plus programmé à 4 min 30.
- Le nouveau runtime E5 écrit dans des panneaux historiques masqués dans la coque mobile WP35 (`driver-alert-panel` / `map-alert-strip`) ; il n’existe pas encore de surface E5 mobile autoritaire dédiée dans `#ar-mobile-nav`.
- Deux systèmes visuels coexistent encore pour le virage simulé (`ar52815Alert` historique + `AllRoadsAlertRuntime`) : ce n’est pas conforme à la règle propre « une autorité par comportement ».
- Plusieurs alertes GPS/réseau/recalcul écrivent directement dans `updateDrivingAssistant` et contournent la priorité E5 ; une alerte moins prioritaire peut donc écraser une alerte critique dans l’assistant.
- Le rappel vocal court annoncé n’est pas réellement planifié : `vocalize()` n’est appelé que lors d’un changement d’alerte prioritaire.
- L’alerte `simulation:virage` n’est pas explicitement résolue à la fin/au redémarrage de la simulation, risque d’état périmé.
- Les 239 tests passent et les scripts JS sont valides, mais les tests E5 actuels sont structurels et ne couvrent ni visibilité WP35, ni cycle publish/resolve, ni priorité face aux alertes GPS, ni déclenchement temporel de la démo.
- Décision d’audit : ne pas empiler de correctif. Prochaine correction E5 devra d’abord consolider une autorité unique, un affichage mobile unique et un banc de test court/déterministe avant d’intégrer les sources une par une.


## 2026-09-09 — E5 nettoyage structurel avant tests WP35
- Nettoyage effectué avant tout nouvel essai utilisateur : suppression des deux anciens panneaux d’alertes masqués et du renderer historique `ar52815Alert`.
- `AllRoadsAlertRuntime` est désormais l’unique autorité de priorité, de rendu mobile et de voix pour les alertes E5 ; la surface existante flash + mini est pilotée uniquement par ce runtime.
- Priorité conservée : danger > sécurité > navigation > information. Le danger critique affiche un flash à son apparition, reste visible en mini, annonce complète une fois puis rappel court toutes les 15 s tant qu’il reste prioritaire.
- GPS incertain/perdu/erreur, perte réseau, blocage HGV et alertes route passent par le runtime ; leurs états sont résolus explicitement au retour à la normale.
- La simulation ne double plus l’alerte et résout `simulation:virage` à l’arrêt/redémarrage, donc aucun état périmé.
- Tests historiques adaptés aux nouveaux points d’autorité au lieu d’exiger les panneaux supprimés. Contrôles : 240/240 tests réussis, 20 scripts JavaScript valides, frontends miroirs identiques.
- E5 reste **en cours** : aucun test WP35 demandé tant que le banc d’essai court/déterministe n’est pas lui-même préparé et contrôlé.

## 2026-09-09 — E5 passe vocale + simulation sans GPS
- Règle vocale centralisée : 3 annonces maximum par alerte ; plus de rappel temporel infini.
- Danger géolocalisé de la simulation : annonces à 300 m, 100 m, entrée ; une seule annonce de fin de zone.
- Visuel « Virage dangereux » conservé tel que validé par Jean-Paul.
- Anomalie repérée pendant le test corrigée : le timer de vitesse générique écrasait la vitesse du scénario long ; le scénario long est désormais l'unique autorité de vitesse et suit les limitations simulées.
- Correction de cohérence : après ajout des étapes danger, la fin du scénario pointe bien sur l'étape finale 10.
- Contrôles : 241 tests réussis ; JavaScript valide ; frontends synchronisés.
- E5 reste à tester par Jean-Paul en simulation sans GPS ; aucun commit avant validation.


## 2026-09-09 — Gel E5 et passe balai pré-E6
- Validation utilisateur E5 acquise sur WP35 en simulation sans GPS : visuel danger, 3 annonces vocales, annonce unique de fin, instructions, limitations et seuils compteur +3 % / +5 %.
- E5 passe officiellement à **terminée**.
- Frontière confirmée : E3 = GPS réel/progression en mouvement ; E4 = sortie d’itinéraire/recalcul ; E6 = essai routier réel, sans absorber E4.
- Audit pré-E6 : contrôle des autorités GPS/alertes, recherche de reliquats historiques et vérification de non-régression avant toute nouvelle fonction.
- Les appels historiques liés au recalcul/retournement restent volontairement hors E5 et seront traités dans E4, afin de ne pas modifier une fonction validée pendant le gel E5.


## 2026-09-09 — Audit pré-E7 vue de conduite réelle
- E6 essai routier est volontairement mis en attente : la scène synthétique E2 reste un bon banc de simulation mais n'est pas une vue de navigation routière exploitable.
- E7 est insérée avant E6 comme chantier « Vue de conduite réelle » ; les étapes fonctionnelles suivantes sont décalées d'un numéro sans changement de contenu.
- Audit du frontend : la carte Leaflet, la géométrie de route, le marqueur véhicule GPS, `routeProgressAt`, la caméra `focusDrivingRoute` et la logique d'orientation existent déjà. Il n'est donc pas nécessaire de réécrire la navigation ni de changer de technologie.
- Conflit principal identifié : les règles E2 masquent volontairement les panes Leaflet et imposent le canvas synthétique pour toute conduite, y compris le mode GPS réel. E7 devra séparer explicitement `conduite réelle` et `simulation`, avec une seule autorité visuelle dans chaque mode.
- Le GPS réel met déjà à jour le marqueur et la vue ; E7 ne doit pas créer de second `watchPosition`, de second moteur de progression ni de seconde autorité de vitesse.
- Plusieurs fonctions historiques de caméra/rotation existent encore (`setDrivingBearing`, `focusDrivingRoute`, styles de caméra). Elles doivent être réutilisées ou consolidées, pas doublées par une nouvelle caméra concurrente.
- Le HUD, E5, les limitations, les instructions et le compteur restent hors du périmètre visuel E7 sauf raccord nécessaire ; ils sont considérés comme acquis à protéger.
- Baseline avant développement E7 : 241 tests réussis. Aucun code fonctionnel E7 ajouté pendant cet audit.


## 2026-09-09 — E7 première passe fonctionnelle : deux points de vue
- E7 sépare désormais explicitement les autorités visuelles : GPS réel = carte Leaflet réelle ; simulation sans GPS = canvas synthétique E2 conservé.
- Aucun nouveau GPS, moteur de vitesse, progression ou itinéraire n'a été créé. La caméra réutilise `focusDrivingRoute` et l'orientation existante.
- Deux cadrages sur la même navigation : « dans le véhicule » par défaut (zoom plus proche, véhicule masqué) et « au-dessus du véhicule » (zoom plus large/reculé, véhicule visible).
- Un seul bouton bascule le cadrage sans recalcul ni rechargement ; le choix est mémorisé localement. Le bouton est masqué en simulation pour ne pas perturber le banc E2/E5.
- Le marqueur de conduite suit maintenant chaque position GPS fiable avant le recentrage caméra, au lieu de rester sur le point de départ.
- Contrôles : 246 tests réussis ; 18 scripts JavaScript valides ; frontends miroirs identiques.
- E7 passe à « à tester par moi » ; aucun commit avant validation utilisateur.

## 2026-09-09 — E7 passe UI complète avant nouveau test
- Retour WP35 intégré : en paysage la zone de conduite était trop comprimée ; en portrait Retour/Accueil manquaient de contraste ; le bouton ARRÊT Bus devait être présent avant validation visuelle.
- Autorité visuelle corrigée : dès l'entrée en conduite réelle (hors Démo sans GPS), la carte Leaflet reprend la main même avant le premier fix GPS ; le canvas E2 reste réservé à la simulation.
- Barre haute conduite : Retour/Accueil renforcés par contraste sans augmenter la hauteur ; en portrait les libellés sont remplacés par les symboles dans des boutons 34 px.
- Mode Bus : emplacement visuel définitif du bouton rouge ARRÊT ajouté en portrait/paysage. Sa mémorisation fonctionnelle reste volontairement E8 ; l'appui E7 n'enregistre aucune donnée.
- Paysage conduite : panneau bas compacté à 78 px et réorganisé pour rendre davantage de hauteur à la route.
- Contrôles : 249 tests réussis ; 20 scripts JavaScript valides ; frontends miroirs identiques. E7 reste à tester par Jean-Paul, aucun commit.

- E7 paysage : barre basse ramenée à une seule ligne compacte dans le cadre existant ; boutons redimensionnés, aucune hauteur de route sacrifiée. Retour/Accueil harmonisés sur Préparer et Prêt. Portrait conduite gelé. 249 tests OK.

## 2026-09-09 — E7 correction ciblée portrait/paysage après retour WP35
- Portrait : le cadre validé est conservé ; seule la répartition des quatre actions basses Bus est harmonisée selon l'espace disponible. L'icône rapport reste carrée, ARRÊT conserve sa priorité visuelle, retournement et blocage occupent le reste sans agrandir le panneau.
- Paysage : la barre basse validée reste inchangée en hauteur et en organisation.
- Cause visuelle paysage traitée dans la scène photo : les assets historiques étaient tous en 900×1200 (portrait). Des variantes paysage 16:9 dédiées sont générées pour les 10 scènes, et la scène sélectionne automatiquement l'asset portrait ou paysage selon l'orientation.
- Le cadrage paysage utilise désormais `cover` et se recale automatiquement lors d'un changement d'orientation ; aucun changement de moteur GPS, vitesse, HUD, alertes ou barre basse.
- Contrôles : 252 tests réussis ; 18 scripts JavaScript valides ; frontends et assets paysage miroirs identiques ; `git diff --check` propre.
- E7 reste **à tester par moi** ; aucun commit avant validation utilisateur.

### 2026-09-09 — E7 passe cadrage paysage + boutons portrait
- Portrait : quatre actions basses conservées dans le cadre validé ; icône carrée + trois boutons texte de largeur égale.
- Paysage : barre basse gelée à 58 px ; suppression du bloc E7 concurrent à 78 px.
- Scène N116 paysage remplacée par un visuel 16:9 natif 1600×900 issu du visuel E7 validé, au lieu du recadrage flou 900×506.
- E7 reste à tester par Jean-Paul ; aucun commit avant validation.


## 2026-09-09 — E7 passe pré-test route
- Régression corrigée : les vues Préparer / itinéraire prêt rendent de nouveau les tuiles Leaflet, même après une simulation.
- Paysage simulation : scène ancrée en bas pour conserver chaussée et véhicule dans la zone utile.
- Portrait et barre basse paysage validés précédemment laissés inchangés.
- Contrôles : 254 tests réussis ; JavaScript vérifié ; miroirs frontend synchronisés.
- E7 reste à tester par Jean-Paul avant commit.

## 2026-09-09 — E7 nettoyage autorité visuelle (option B)
- Audit confirmé : plusieurs règles historiques se disputaient encore l'affichage de Leaflet, du décor photo et du canvas synthétique selon Préparer / Prêt / Conduite.
- Nettoyage ciblé effectué sans refonte : suppression du socle photo historique sur Préparer/Prêt ; Leaflet devient l'unique décor de ces deux états.
- La classe `ar52620-demo-camera` n'est désormais active qu'en conduite simulée ; elle est retirée avant Préparer/Prêt et en conduite GPS réelle.
- Le canvas synthétique E2 est désormais explicitement limité à `Démo sans GPS + Conduite`; il ne masque plus Leaflet par une règle générique de conduite.
- Le décor photo du scénario Bus est lui aussi limité à la simulation en conduite ; un aperçu d'itinéraire réel ne peut plus activer ce décor.
- Les transitions de panneau nettoient les traces de scène/démo hors conduite, afin qu'un retour vers Préparer reparte sur une carte propre.
- Contrôles : 259 tests réussis, 20 scripts JavaScript valides, miroirs frontend identiques, `git diff --check` propre.
- E7 reste à tester sur WP35 avant tout commit : Préparer → Prêt → Démo → Retour → Préparer → Conduite réelle.

## 2026-09-09 — reconstruction ciblée brique cartographie/conduite
- Abandon des rustines visuelles concurrentes.
- Suppression des anciennes autorités de visibilité carte/photo/canvas devenues conflictuelles.
- Mise en place d’une autorité visuelle unique par état via `data-ar-visual-mode`.
- Préparer revient sur une vue Europe ; Prêt et Conduite réelle restent Leaflet ; Démo sans GPS reste synthétique.
- Contenu historique placé après `</html>` rapatrié dans le document HTML valide ; autorité finale placée en dernier.
- 251 tests réussis ; scripts JavaScript validés ; E7 reste à tester sur WP35.

## 2026-09-09 — reconstruction ciblée brique cartographie/conduite
- Abandon des rustines visuelles concurrentes.
- Suppression des anciennes autorités de visibilité carte/photo/canvas devenues conflictuelles.
- Mise en place d’une autorité visuelle unique par état via `data-ar-visual-mode`.
- Préparer revient sur une vue Europe ; Prêt et Conduite réelle restent Leaflet ; Démo sans GPS reste synthétique.
- Contenu historique placé après `</html>` rapatrié dans le document HTML valide ; autorité finale placée en dernier.
- 251 tests réussis ; 19 scripts JavaScript validés ; E7 reste à tester sur WP35.


## 2026-09-09 — E7 reconstruction page blanche ciblée de la brique cartographie/conduite
- Décision validée : ne plus réparer l’ancien empilement visuel ; reconstruire uniquement la brique E7, sans réécrire AllRoad’s.
- Autorité unique `AllRoadsVisualBrick` : Préparer=Leaflet Europe, Prêt=Leaflet + tracé, Conduite réelle=Leaflet, Démo sans GPS=canvas synthétique.
- Correction d’un conflit d’état important : `previewExisting()` quitte maintenant explicitement le mode démo avant tout calcul réel.
- Préparer réactive explicitement une couche Leaflet et recadre l’Europe ; la carte n’est plus dépendante d’un ancien état de conduite.
- La démo ne crée plus l’ancien marqueur Bus Leaflet et ne réactive plus les anciens décors photo/WebGL. Le canvas synthétique ne tourne qu’en mode démo.
- En vue conducteur, aucun véhicule propre n’est dessiné ; en vue dessus, le canvas utilise une silhouette neutre reconstruite, indépendante de l’ancien Bus de démonstration.
- GPS, routage, E5 alertes, HUD, STOP Bus visuel et coque responsive sont conservés ; aucun second moteur GPS/vitesse/progression n’a été ajouté.
- Contrôles : 253 tests réussis ; 19 scripts JavaScript valides ; miroirs frontend identiques ; `git diff --check` propre.
- E7 reste **à tester par moi** sur WP35 avant commit.

### 2026-09-09 — E7 entrée Préparer isolée
- Après test WP35, Ready et Conduite réelle affichent correctement Leaflet ; défaut isolé à Préparer.
- Préparer utilise désormais une entrée cartographique dédiée : couche mobile explicite + cadrage Europe fixe + redraw, sans GPS automatique.
- Statut : à tester par Jean-Paul sur WP35.

### 2026-09-09 — E7 entrée Préparer isolée
- Après test WP35, Ready et Conduite réelle affichent correctement Leaflet ; défaut isolé à Préparer.
- Préparer utilise désormais une entrée cartographique dédiée : couche mobile explicite + cadrage Europe fixe + redraw, sans GPS automatique.
- Statut : à tester par Jean-Paul sur WP35.

## 2026-09-09 — E7 ménage général des appels d’état
- Retour WP35 : Préparer restait vide, tandis que l’Europe apparaissait brièvement dans `Itinéraire prêt`. Cela confirmait un appel différé survivant au changement d’écran.
- Audit général : `panel()` était réassigné par un wrapper historique ; `clearDrivingBearing()`/`restoreDrivingBaseLayer()` pouvaient intervenir lors d’une sortie de conduite ; plusieurs `setTimeout` recadraient la carte après que l’état avait déjà changé.
- Nettoyage structurel : suppression du wrapper `oldPanel`; un seul `function panel(state)` demeure. Ajout d’un compteur d’état `arE7StateEpoch` : toute tâche d’affichage programmée par un ancien état est abandonnée dès qu’une nouvelle transition commence.
- L’ouverture rend désormais la coque cartographique visible avant d’entrer dans `prepare`, puis le contrôleur cadre Europe après deux frames de rendu. Aucun timer Europe ne peut ensuite déborder dans `ready`.
- `AllRoadsVisualBrick` ne pilote plus Leaflet : il ne choisit que le mode visuel CSS. Le contrôleur E7 est seul propriétaire des couches/cadrages Leaflet pour Préparer/Prêt/Conduite.
- Les anciens recadrages différés de démarrage réel et d’orientation ont été raccordés au même contrôleur avec vérification de l’état courant.
- Contrôles : 260 tests réussis ; 19 scripts JavaScript inline valides ; `/`, `/version`, `/app/` = HTTP 200 ; miroirs frontend identiques ; `git diff --check` propre.
- Statut : E7 **à tester par moi** sur WP35. Aucun commit avant validation.

## 2026-09-09 — E7 chasse aux fantômes / ménage profond de la brique cartographie
- Retour WP35 confirmé : la carte Europe apparaissait encore fugitivement dans `Itinéraire prêt`, tandis que Préparer restait vide. La transition vers `ready` avait donc encore lieu avant que l'itinéraire soit réellement prêt.
- Nettoyage global de la brique : suppression des anciens helpers `ar52992*` de cadrage national, retrait complet de l'ancien moteur photo et de l'ancien moteur WebGL de démonstration. Leurs fichiers/assets ne sont pas supprimés du projet, mais ils ne sont plus appelés par E7.
- `panel(state)` reste l'unique contrôleur d'état. Toute tâche cartographique différée est annulée à chaque transition par `arE7CancelDeferred()` et protégée par un numéro d'état.
- Préparer utilise désormais un cycle d'activation Leaflet contrôlé : couche mobile explicite, vérification que le conteneur a une taille réelle, `invalidateSize`, cadrage Europe, puis `redraw`. Les rares retries sont annulés si l'écran change.
- Le bouton `Afficher l'itinéraire` ne passe plus immédiatement à `ready`. E7 reste en Préparer pendant le calcul et ne bascule en `Itinéraire prêt` qu'à réception de l'événement réel `allroads:route-ready`.
- Le moteur de calcul général ne fait plus lui-même un `fitBounds` lorsqu'E7 mobile est ouvert : le contrôleur E7 est seul propriétaire du cadrage. Cela retire la dernière course entre la carte Europe et la carte de l'itinéraire.
- Le lanceur utilise un nouveau jeton de build `e7ghostclean1` afin de forcer une navigation fraîche sur WP35 sans changer la version produit V52.9.95.
- Audit statique final : 1 `panel(state)`, 1 brique visuelle E7, 1 script de brique visuelle, 1 `watchPosition`; aucune référence restante aux helpers nationaux historiques, au moteur photo ou au moteur WebGL.
- Contrôles : 265 tests réussis ; 19 scripts JavaScript inline valides ; miroirs frontend identiques ; `git diff --check` propre.
- Statut : E7 **à tester par moi** sur WP35. Aucun commit avant validation.


## 2026-09-09 — E7 — isolation physique carte / démo
- La capture Démo sans GPS a révélé que le canvas synthétique était encore enfant de la carte Leaflet et n'avait ni positionnement plein écran ni dimensions CSS explicites.
- Conséquence observée : une dalle bleue synthétique ne couvrait qu'une partie du viewport tandis que Leaflet restait visible dessous. Cela confirme une coexistence de deux couches visuelles au lieu d'une exclusivité réelle.
- Correction structurelle : canvas sorti de `#map`, placé dans `#ar-e7-demo-layer` fixe plein écran ; plus aucune règle E7 ne masque individuellement les panes Leaflet.
- Jeton launcher : `e7layersplit1`.
- Validation automatique : 268 tests OK avant packaging.

## 2026-09-09 — E7 Préparer isolé sur une couche Leaflet fraîche
- Les tests WP35 valident Démo sans GPS, Itinéraire prêt et Conduite réelle ; seul Préparer reste vide.
- Préparer n'utilise désormais plus la couche Leaflet déjà vécue par les autres états : il crée une couche de tuiles fraîche à l'entrée, après affichage réel du conteneur, puis la détruit en quittant Préparer.
- Prêt et Conduite réelle récupèrent ensuite la couche cartographique normale existante, sans modification de leurs logiques validées.
- Le changement Carte/Relief/Satellite dans Préparer reconstruit cette couche dédiée proprement.
- Contrôles : 270 tests réussis ; 19 scripts JavaScript valides ; miroirs frontend identiques ; git diff --check propre.
- Statut : E7 à tester par moi sur WP35 ; aucun commit avant validation.

## 2026-09-09 — E7 Préparer remis à nu puis reconstruit
- Décision produit : arrêter d'essayer de repeindre l'ancien Préparer ; conserver les états Démo, Prêt et Conduite réelle validés, et reconstruire Préparer sur une surface neuve.
- Préparer possède désormais son propre conteneur `#ar-e7-prepare-map` et sa propre instance Leaflet. Il ne partage plus le DOM, les panes, les couches ni le cycle de vie de `#map` utilisé par Prêt/Conduite.
- En mode Préparer, la carte route historique `#map` est physiquement masquée ; seule la nouvelle carte Europe est affichée. En quittant Préparer, cette surface est masquée et `#map` reprend la main sans modification de Prêt/Conduite.
- Carte / Relief / Satellite dans Préparer reconstruisent uniquement la couche de la carte de préparation ; elles ne manipulent plus la carte route tant que l'état est Préparer.
- Cette séparation rend inoffensives les anciennes règles CSS visant `#map` dans Préparer : elles ne peuvent plus recouvrir ou neutraliser la nouvelle surface.
- Contrôles : 271 tests réussis ; 19 scripts JavaScript valides ; miroirs frontend identiques ; `git diff --check` propre.
- Jeton launcher : `e7preparebare1`. Statut : **à tester par moi** sur WP35 ; aucun commit avant validation.


## 2026-09-09 — E7 réparation de la chaîne après Préparer à nu
- Retour WP35 : après l’ajout de la surface Préparer dédiée, la navigation pouvait rester bloquée entre Accueil et Véhicule.
- Cause identifiée : la nouvelle surface fixe de Préparer était pilotée par `data-ar-visual-mode=prepare` même lorsque la navigation route était fermée. Elle pouvait donc rester active hors de la chaîne itinéraire et intercepter l’interface.
- Correction : les surfaces E7 Préparer et Démo sont désormais strictement limitées à `body.ar-mobile-nav-open`; hors navigation route, le contrôleur passe en mode `off` et les surfaces sont forcées masquées. `close()` et `backToVehicle()` libèrent explicitement la brique visuelle.
- Les états déjà validés Prêt / Conduite réelle / Démo ne sont pas modifiés fonctionnellement.
- Contrôles : 274 tests réussis. Statut : à tester par moi sur WP35. Jeton launcher `e7chainsafe1`.


## 2026-09-09 — E7 nettoyage ciblé du retour vers Préparer
- Décision utilisateur : ne plus retoucher les états Prêt / Conduite réelle / Démo validés ; traiter uniquement la transition arrière vers Préparer.
- Ajout d’une routine unique `arE7ResetForPrepare()` appelée par Retour depuis Itinéraire prêt et par Modifier.
- Cette routine arrête GPS/simulation, retire marqueurs/casing/tracé de route, nettoie les anciennes classes photo/caméra, supprime les transformations/masques inline des panes Leaflet, restaure la couche cartographique normale puis laisse `panel('prepare')` recadrer l’Europe.
- Aucun nouveau moteur ni nouvelle surface n’est ajouté. Le but est de revenir à une carte Préparer propre au lieu d’empiler une couche supplémentaire.
- Jeton launcher : `e7backclean1`.
- Contrôles : 269 tests réussis ; 19 scripts JavaScript inline valides ; miroirs frontend identiques ; `git diff --check` propre.
- Statut : **à tester par moi** sur WP35 ; aucun commit avant validation.

## 2026-09-09 — E7 décapage Préparer après audit historique
- Audit comparatif V52.9.95 / premières passes E7 : les anciennes règles V52.8.x pouvaient imposer un fond vert et réduire les tuiles Leaflet en Préparer.
- Décapage de `allroads_ui_final.css` : une seule autorité Préparer/Ready, Leaflet à 100 %, aucun voile/photo/canvas/pseudo-calque avant conduite.
- Suppression de la dernière règle tardive qui repeignait aussi `#map` en Préparer.
- Restauration de l'ordre d'ouverture observé dans la V52.9.95 saine : état Préparer posé avant ouverture de la coque, puis recalcul Leaflet après affichage.
- Conduite réelle, Démo sans GPS et Itinéraire prêt non modifiés fonctionnellement.
- Vérifications : 272 tests OK, 19 scripts JS inline valides, miroirs HTML/CSS identiques, `git diff --check` propre.
- Statut : E7 à tester par Jean-Paul sur WP35. Pas de commit avant validation téléphone.

## 2026-09-09 — audit chaîne mouvement réel avant essai route
- Audit sans modification fonctionnelle, après validation visuelle Préparer → Prêt → Conduite → Retour.
- Chaîne vérifiée : `watchPosition` unique → qualification précision GPS → vitesse native ou delta fiable → `routeProgressAt()` → `updateGpsGuidance()` → HUD → `focusDrivingRoute()`.
- Points sains : un seul `watchPosition`; aucun mouvement inventé sans fix fiable; vitesse `--` avant mesure; GPS incertain conserve le dernier fix fiable; GPS perdu arrête l'estimation; progression et guidage utilisent la géométrie calculée.
- Blocage critique identifié avant essai route : `focusDrivingRoute()` appelle `syncMobileDriveMarker()` à chaque fix. Cette fonction recrée actuellement `mobileDriveMarker` au premier point de l'itinéraire avant que la caméra lise sa position. Le callback GPS place bien le marqueur à la position réelle, mais `focusDrivingRoute()` peut aussitôt le remettre au départ. Cela peut empêcher le mouvement réel d'être visible malgré un GPS correct.
- Dette secondaire repérée : l'ancien moteur de simulation `navLaunchButton` (requestAnimationFrame) est encore présent en parallèle du moteur Démo E7, même s'il n'est pas le chemin normal de la conduite E7. À neutraliser ou isoler plus tard sans casser la démo validée.
- Aucune modification de code métier pendant cet audit. `pytest -q` : 272 tests réussis.

## 2026-09-09 — E3 réparation raccord GPS → marqueur → caméra
- Correction ciblée du blocage identifié pendant l’audit mouvement réel ; aucune modification de Préparer, Itinéraire prêt, Démo, E5 ou du moteur de routage.
- `syncMobileDriveMarker()` ne recrée plus le véhicule au premier point de la route à chaque recentrage.
- En conduite réelle, `vehicleMarker` alimenté par `watchPosition` est l’unique source permettant de créer le marqueur de conduite ; sans premier fix GPS fiable, aucun faux véhicule n’est placé au départ.
- Une fois créé, `mobileDriveMarker` conserve sa position et chaque fix GPS le déplace sur `currentPos` avant l’appel de `focusDrivingRoute()`.
- Ajout de tests de non-régression dédiés au raccord GPS/marqueur/caméra.
- Contrôles : 275 tests réussis. Statut E3 : **à tester par moi** sur WP35 en mouvement réel avant E6.

## 2026-09-09 — E7 caméra GPS conducteur à tester
- Conduite réelle uniquement : la carte Leaflet tourne désormais selon le cap de la route.
- Le cadrage regarde devant le véhicule le long de l'itinéraire, au lieu d'afficher l'ensemble du trajet.
- Vue conducteur : zoom 19 sous 70 km/h, zoom 18 à partir de 70 km/h ; vue dessus conservée à 17.
- Aucun changement du GPS, du calcul d'itinéraire, de Préparer, de Prêt, de la Démo ou des alertes E5.
- Statut : à tester sur WP35 en condition réelle.

## 2026-09-10 — Raccord saisie trajet → géocodage réel
- Correction prioritaire avant essai route : l'écran mobile géocode désormais le départ ET la destination visibles avant tout calcul.
- Les anciennes coordonnées Ille-sur-Têt / Vinça ne peuvent plus être réutilisées silencieusement pour un trajet saisi différent.
- « Ma position » utilise une position GPS réelle (position connue ou acquisition ponctuelle), jamais les coordonnées de démonstration.
- Aucun changement de caméra, E5, Préparer/Prêt ou moteur de routage.
- Tests automatiques : 280 réussis. Statut : à tester par Jean-Paul sur WP35.

## 2026-09-10 — Géocodage ambigu : proximité du trajet
- Correction du bug pouvant envoyer un nom local ambigu vers un homonyme mondial.
- La destination est maintenant géocodée après le départ, avec le départ comme point de proximité.
- Le backend transmet ce point de proximité à Pelias/ORS.
- Aucun trajet longue distance n’est interdit : la proximité sert au classement, pas à bloquer un vrai voyage international.
- Tests automatiques : 283 réussis. Statut : à tester par Jean-Paul.

## 2026-09-10 — Géocodage : homonymes réellement reclassés
- Test WP35 : « Ma position → Vinça » calculait encore 10 519 km jusqu’en Afrique de l’Est.
- Cause vérifiée : `focus.point` était seulement transmis à Pelias/ORS, mais AllRoad’s prenait ensuite aveuglément `places[0]`. Le fournisseur ne garantit pas que le candidat le plus proche soit le premier.
- Correction : demander jusqu’à 10 candidats puis, lorsqu’un départ réel est connu, les reclasser côté AllRoad’s par distance au départ avant de renvoyer les 5 meilleurs.
- Aucun changement caméra, E5, Préparer/Prêt ou moteur de routage.
- Tests : 285/285.
- Statut : à tester par moi sur WP35, d’abord Ma position → Vinça.

## 2026-09-10 — Géocodage : cause du faux départ « Ma position » isolée et corrigée
- Diagnostic de la chaîne complète après les trajets aberrants Bulgarie/Tanzanie : le géocodeur n'était pas seul en cause.
- Cause certaine côté départ : `arE7ResolveRoutePoint("Ma position")` réutilisait `vehicleMarker` si présent. Or ce marqueur Leaflet est aussi utilisé/déplacé par la démo et d'anciens trajets ; il pouvait donc fournir une fausse « position GPS ».
- Correction propre : « Ma position » ne lit plus jamais un marqueur cartographique. Une mesure `navigator.geolocation.getCurrentPosition` fraîche est obligatoire, contrôlée puis utilisée comme départ et comme point de proximité pour la destination.
- Aucun changement caméra, E5, Préparer/Prêt ou moteur de routage.
- Statut : à tester par Jean-Paul sur WP35 avec Ma position → Vinça, puis un second lieu local différent.
\n## 2026-09-10 — Blocage identifié : page WP35 réutilisée entre correctifs\n- Le lanceur conservait le même URL `build=e3gpsmarker1` malgré les nouvelles archives. Android/Chrome pouvait donc simplement remettre au premier plan le document déjà ouvert au lieu de charger le frontend corrigé.\n- Cela explique qu’un changement de destination puisse sembler sans effet malgré un code source corrigé.\n- Jeton de lancement remplacé par `geofresh1` afin de forcer une navigation fraîche sans toucher au cache métier, aux données ni aux fonctions validées.\n- Géocodage métier inchangé dans cette passe : on vérifie d’abord que WP35 exécute réellement la version testée.\n
## 2026-09-10 — Diagnostic visible chaîne géocodage
- Après plusieurs corrections non concluantes, aucun nouveau comportement de géocodage n'est modifié.
- Ajout temporaire d'un diagnostic visible WP35 affichant : demande saisie, coordonnées de départ réellement retenues, résultat destination retenu, puis coordonnées effectivement envoyées au moteur de routage.
- Objectif : localiser précisément la rupture entre GPS réel, géocodeur et paramètres du routeur avant toute nouvelle correction.
- Jeton launcher `geodiag1` pour garantir le chargement de cette instrumentation.
- Contrôles : 290 tests réussis, 19 blocs JavaScript valides, miroirs frontend identiques. Statut : à tester par Jean-Paul.

## 2026-09-10 — diagnostic source « Ma position »
- Le diagnostic WP35 a isolé la panne : Thuir est correctement géocodé en France, tandis que `navigator.geolocation.getCurrentPosition()` fournit un départ en Tanzanie ; le géocodeur destination n'est donc pas modifié.
- Passe diagnostic uniquement : `Ma position` exige désormais une mesure navigateur fraîche (`maximumAge: 0`) et le bandeau affiche aussi la précision annoncée et l'heure de cette mesure.
- Aucun contournement ni coordonnée forcée n'est ajouté : le but est de déterminer si Android/Chrome livre une position fraîche mais fausse, ou une mesure de mauvaise qualité/périmée.
- Statut : à tester sur WP35 avec Ma position → Thuir.

## 2026-09-10 — Consolidation « Ma position » sur l’autorité GPS E3 — à tester
- Diagnostic WP35 : la destination Thuir est correctement géocodée ; le départ « Ma position » recevait une coordonnée aberrante.
- Nettoyage ciblé : `arE7ResolveRoutePoint()` n’appelle plus directement `getCurrentPosition()` et ne lit aucun marqueur Leaflet pour « Ma position ».
- Toute acquisition de départ passe maintenant par `AllRoadsGpsRuntime.requestFreshPosition()`, qui utilise le même fournisseur `watchPosition` que la conduite E3 et n’accepte qu’un fix avec précision <= 50 m.
- Le point d’appel natif `navigator.geolocation.watchPosition()` est centralisé dans un seul helper ; aucune logique de géocodage destination, caméra, E5 ou cartographie n’a été modifiée.
- Jeton de lancement WP35 : `gpsauthority1`.
- Contrôles : 293 tests réussis ; 19 scripts JavaScript inline valides ; miroirs frontend identiques.
- Statut : **à tester par moi** avec `Ma position → Thuir` avant toute autre correction.


## 2026-09-10 — « Ma position » : recherche GPS anticipée, position jamais anticipée — à tester
- Décision produit figée : AllRoad’s peut anticiper la recherche du signal GPS, jamais la position elle-même.
- Dès l’entrée dans Préparer, l’autorité GPS E3 ouvre une écoute haute précision sans calculer ni déplacer l’itinéraire.
- « Ma position » n’accepte qu’un fix frais (horodatage <= 15 s) et fiable (précision <= 50 m). Aucune ancienne destination, aucun marqueur et aucune estimation ne peuvent servir de départ.
- Si le conducteur demande « Ma position » avant un fix valable, le calcul attend puis affiche « Recherche de votre position GPS… » au lieu d’utiliser une coordonnée de secours. Un départ saisi manuellement reste disponible.
- Au passage en conduite réelle, l’écoute de préparation est fermée avant l’écoute GPS de conduite : une seule écoute native active à la fois.
- Géocodage villes/adresses, caméra, E5 et cartographie inchangés. Jeton WP35 `gpsprepare1`.
- Contrôles : 296 tests réussis ; 19 scripts JavaScript inline valides ; miroirs frontend identiques. Statut : à tester par Jean-Paul.

## 2026-09-10 — Géocodage intermittent : panne fournisseur distinguée d’une adresse inconnue
- Le GPS fiable validé reste inchangé.
- Cause de faux message identifiée : une exception réseau ORS/Pelias était convertie en liste vide, donc affichée comme « adresse introuvable ».
- Correction ciblée : deux essais identiques du géocodeur ; si le fournisseur reste indisponible, réponse 503 explicite au lieu d’une fausse adresse inconnue.
- Une vraie réponse vide reste seule à produire « adresse introuvable ».
- Contrôles : 298 tests réussis ; JavaScript valide ; miroirs frontend identiques. Statut : à tester par moi sur WP35.

## 2026-09-10 — V52.9.97 rollback sélectif DIAG, règle GPS conservée — à tester
- Retour arrière ciblé : suppression complète de la fenêtre temporaire `DIAG GÉOCODAGE` et de son instrumentation dans le submit historique.
- Aucun changement du moteur de routage, de Leaflet, de la conduite ou du passage `allroads:route-ready`.
- La règle GPS validée est conservée : autorité `AllRoadsGpsRuntime`, écoute anticipée en Préparer, fix frais et fiable, aucune position inventée/réutilisée.
- But unique du test : vérifier si le passage Itinéraire prêt → conduite revient après retrait du bloc diagnostic, sans perdre la correction GPS.
- Jeton WP35 `rollbackdiag1`.


## 2026-09-10 — V52.9.102 — Barre de conduite minimaliste
- Base : V52.9.97 validée sur WP35, chaîne GPS → géocodage → routage laissée intacte.
- En conduite, la barre complète reste visible au départ puis se rétracte après ~4,2 s sans interaction.
- Un toucher de la carte la fait réapparaître temporairement.
- Arrêt réel confirmé : vitesse <= 0,8 km/h pendant ~3 s → barre complète affichée automatiquement.
- Reprise confirmée >= 2 km/h → barre visible brièvement puis rétractée.
- Mode Bus : bouton ARRÊT reste accessible même barre rétractée.
- Distance restante et temps estimé restent visibles dans un panneau translucide superposé à la carte.
- Statut : à tester par Jean-Paul sur WP35.


## V52.9.102 — barre conduite à l’arrêt temporisée
- Base : V52.9.99 validée pour l’accès à la vue conduite.
- À l’arrêt confirmé, la barre reste visible 20 s puis se rétracte une seule fois.
- Aucun cycle de réapparition automatique. Un toucher de la carte/écran la rappelle et relance 20 s.
- En mouvement, temporisation courte conservée (~4,2 s).
- En Bus, ARRÊT reste disponible lorsque la barre est masquée.
- GPS, géocodage et routage inchangés.


## V52.9.102 — conduite minimaliste : incrustations + ARRÊT Bus permanent
- Barre rétractée : ARRIVÉE, RESTE et TEMPS restent visibles comme trois incrustations semi-transparentes indépendantes sur la carte, sans fond de barre.
- Bus : ARRÊT reste visible sous forme de bouton rond rouge indépendant lorsque la barre est masquée.
- Barre visible : pas de doublon des incrustations.
- Aucun changement GPS, géocodage ou routage.


## 2026-09-10 — V52.9.109 — Vue véhicule pré-tests
- Après le nettoyage 108, cause du véhicule absent isolée : le bloc visuel E7 masquait explicitement `#ar5268-drive-vehicle` en caméra `driver`.
- Correction ciblée : le véhicule HUD est désormais visible en vue conduite uniquement lorsqu'il a été créé à partir d'un ancrage GPS réel ; aucun véhicule n'est inventé sans fix.
- Caméra véhicule recentrée pour placer l'ancrage vers 72 % de la hauteur et ouvrir le zoom selon la vitesse afin de montrer davantage de route devant.
- Aucun changement GPS, géocodage ou routage. Statut : à tester sur WP35.

- Contrôles finaux : 304 tests réussis ; 20 scripts JavaScript inline valides ; miroirs frontend identiques.

## V52.9.110 — Orientation carte seule
- Après validation de la base nettoyée 108, ordre de travail fixé pour les pré-tests : orientation, puis zoom, puis véhicule.
- 110 ne traite que l'orientation de la carte en conduite.
- Le zoom courant est conservé et le véhicule HUD est volontairement masqué.
- Le cap utilise la géométrie du trajet, avec priorité au segment devant un GPS réel s'il existe.
- Chaîne GPS / géocodage / routage non modifiée.

## V52.9.111 — 10/09/2026 — Orientation centrée
- V52.9.110 a prouvé que la rotation de carte était active, mais le trajet sortait de la zone utile.
- Cause isolée : la rotation utilisait un pivot vertical à 72 % de la hauteur de carte.
- Correction unique : pivot de rotation ramené au centre réel de la carte (50 % / 50 %).
- Zoom et placement véhicule volontairement laissés inchangés.
- GPS / géocodage / routage non modifiés.

## V52.9.112 — Zoom/cadrage seul
Étape 2 pré-tests : orientation 111 conservée, zoom/cadrage rapproché sur la route à venir. Véhicule HUD toujours masqué. GPS/routage inchangés.

## V52.9.113 — Zoom intermédiaire
- 112 a validé l'effet du zoom mais montré un rapprochement excessif.
- Correction unique : rapprochement ramené de +2 à +1 niveau par rapport au zoom de référence.
- Orientation 111 et logique de cadrage conservées ; véhicule HUD toujours masqué.
- GPS / géocodage / routage non modifiés.

## V52.9.115 — Point conducteur calculé
- Cadrage basé sur la taille réelle de la carte Leaflet.
- Cible : 50 % largeur / 72 % hauteur utile.
- Orientation et zoom conservés ; véhicule toujours masqué.

## V52.9.117 — Zoom mathématique
- Remplacement du dézoom manuel par un calcul fondé sur la taille réelle de la carte et la géométrie réelle de l'itinéraire.
- Point conducteur 50/72 conservé.
- GPS, géocodage et routage non modifiés.

## V52.9.118 — Chasse aux fantômes caméra Conduire
- Audit demandé après V52.9.117.
- Fantôme principal confirmé : rotation Leaflet + `scale(1.18)` créait un second zoom visuel hors calcul Leaflet.
- Les transforms de panes sont maintenant nettoyés avant toute projection/calcule de cadre.
- Centre et orientation utilisent désormais le même axe local de route devant le conducteur.
- Une seule fonction applique centre + zoom + orientation (`arE7ApplyDrivingCamera`).
- Sans position réelle, aucune ancre conducteur n'est fabriquée à partir du départ de l'itinéraire.
- GPS, géocodage et routage inchangés.
- 317 tests verts.

## V52.9.120 — référentiel géométrique caméra
- Surface cartographique utile mesurée depuis le DOM réel.
- Point conducteur calculé dans cette surface : 50 % largeur, 72 % hauteur utile.
- Centre Leaflet obtenu par inversion exacte de la rotation pour placer l’ancre GPS au point conducteur après rotation.
- Aucun décalage empirique WP35 ; GPS/géocodage/routage inchangés.
- Tests : 325/325 verts.


## V52.9.124 — Horizon de conduite dynamique
- Remplacement de l'horizon `65 % du trajet restant` par une distance calculée à partir de la vitesse.
- Fenêtre temporelle : 180 s ; bornes : 1,2 km à 6,5 km.
- La route restante ne peut plus imposer un dézoom excessif ; elle plafonne seulement l'horizon calculé.
- Caméra, GPS et routage : chaîne métier inchangée hors règle d'horizon.

## V52.9.129 — chasse aux fantômes rotation / bandes haut-bas
- Audit 126→127→128 : 127 ne change que l'opacité du bandeau ; 128 ne change que la couche de fond (CARTO → OpenTopoMap). Ces passes ne créent donc pas directement les bandes.
- Cause retrouvée plus en amont : depuis V52.9.118, le `scale(1.18)` arbitraire a été supprimé à juste titre, mais la rotation des panes Leaflet n'avait plus de couverture compensée. Selon angle + ratio du viewport, des coins non couverts apparaissent alors en haut/bas.
- Correction V52.9.129 : facteur de couverture calculé géométriquement depuis largeur/hauteur/angle, puis compensé dans le centrage et le calcul de zoom. Aucun zoom caché constant.
- GPS, géocodage, routage et horizon dynamique inchangés.
- Tests : 335/335 verts ; 20 scripts inline par frontend + JS externes vérifiés ; frontends identiques.


## V52.9.130 — fond de carte stable en rotation
- Fantôme identifié : le rafraîchissement d’orientation rechargeait une couche mémorisée avant la caméra de conduite.
- `clearDrivingBearing()` pouvait aussi restaurer une ancienne couche lors d’un état GPS transitoire.
- Fond de conduite désormais découplé des changements portrait/paysage et pertes GPS momentanées.

## V52.9.131 — fond cartographique choisi persistant
- Diagnostic : `arE7EnsureBaseLayer()` rappelait `enableDrivingBaseLayer()` à chaque rotation, et `enableDrivingBaseLayer()` imposait systématiquement `mapViews.drive` (OpenTopoMap), annulant le choix Satellite/Carte/Relief.
- Nettoyage : en conduite, l'autorité de fond est désormais la préférence utilisateur persistée (`normal`, `complex`, `satellite`). Une rotation/resize ne peut plus substituer OpenTopoMap.
- Aucun changement GPS, géocodage, routage, caméra, horizon ou ruban.
- Tests ciblés V52.9.131 : 2/2 verts.
- Suite générale : 319 verts + 22 tests historiques d'identité de version encore figés sur V52.9.102 (dette de tests préexistante, non liée à la correction 131).

## V52.9.132 — correction lancement WP35
- Fantôme isolé : le BAT 131 attendait `/version = V52.9.131`, mais `APP_VERSION` expose encore V52.9.102 ; l’ouverture ADB était donc bloquée.
- Lanceur réaligné sur la vraie autorité serveur V52.9.102.
- Correction cartographique 131 conservée telle quelle.

## V52.9.135 — diagnostic système Android / barres
- Retour strict sur V52.9.132 validée pour le code applicatif.
- Aucun changement GPS, routage, caméra, cartographie, UI ou responsive.
- Le lanceur lit puis supprime uniquement la politique immersive globale Android `policy_control` avant ouverture Chrome directe.
- But : déterminer si la disparition des barres système vient d’un réglage Android persistant hors AllRoad’s.
- Statut : à tester sur WP35 ; relever `policy_control AVANT/APRES` et présence des barres.

## V52.9.137 — cadrage aperçu avant démarrage
Passe visuelle isolée depuis V52.9.136 : l'aperçu Prêt satellite utilise désormais la géométrie réelle du viewport, le GPS frais et l'axe local de la route pour placer le conducteur à 50 % / 72 % et orienter la route vers le haut. GPS/routage/caméra Conduite inchangés. Validation WP35 requise avant toute décoration.

## V52.9.138 — Ruban métrique gabarit
Ruban bleu calculé depuis la largeur réelle du véhicule +5 %, convertie en pixels selon zoom/latitude. Le gabarit saisi dans « Quel véhicule ? » est l'autorité, permettant les convois exceptionnels sans élargir le standard.


## V52.9.139 — Rapprochement caméra progressif
- Après validation WP35 du ruban métrique V138, réduction de l’horizon de caméra Conduite selon une règle calculée.
- Horizon = max(300 m, 75 s à la vitesse réelle, prochaine manœuvre × 1,25), plafonné à 3,2 km et par la route restante.
- Exemple actuel 450 m à 0 km/h : horizon ≈ 562,5 m au lieu du minimum historique de 1,2 km.
- Aucun changement GPS, géocodage, routage, rotation, point conducteur 50/72 ou largeur métrique du ruban.
- Statut : à tester sur WP35.

## V52.9.140 — Transparence Préparer / Itinéraire prêt + CTA orange
- Habillage uniquement : panneaux Préparer et Itinéraire prêt rendus fortement transparents pour laisser la carte prioritaire.
- Champs et boutons secondaires semi-transparents ; actions principales Afficher l’itinéraire / Démarrer restent bleues.
- « Continuer vers l’itinéraire » passe orange au toucher/clic pendant 180 ms avant la transition.
- Aucun changement GPS, routage, caméra ou ruban métrique.

## V52.9.141 — 2026-09-10
- Harmonisation visuelle des états Préparer et Itinéraire prêt sur la signature de Conduire.
- Barre ALLROAD'S et commandes cartographiques flottantes placées comme en Conduire.
- Grand panneau blanc retiré visuellement ; composants conservés en incrustations transparentes.
- Orange du bouton Continuer vers l’itinéraire corrigé vers #FF8038.
- Chaîne GPS/routage/caméra et ruban métrique laissés inchangés.

## V52.9.146 — vraie vue Itinéraire unique
- Nettoyage du fantôme structurel : PREPARE et READY étaient encore deux panneaux frères.
- READY est maintenant déplacé physiquement dans PREPARE : une carte, une coque, une vue.
- En READY, les champs de préparation restent présents et les résultats/actions apparaissent dans le même panneau.
- Modifier revient à PREPARE sans changer d'écran.
- Portrait : empilé ; paysage : résultats + actions compacts.
- Aucun changement GPS / géocodage / calcul d'itinéraire / caméra / ruban métrique.

## V52.9.147 — nettoyage fantômes itinéraire unique
- Audit V145/V146 : le résultat READY restait une `.ar51-state-panel`, donc encore branché à l'ancienne mécanique de vues et à de nombreuses autorités CSS historiques.
- Suppression de ce lien : READY devient `.ar51-ready-inline`, intégré physiquement dans PREPARE.
- L'état métier `ready` est conservé, mais il n'existe plus de seconde vue visuelle d'itinéraire.
- Hauteurs/overflow READY neutralisés par une autorité finale dédiée.
- GPS / géocodage / routage / caméra / ruban métrique inchangés.


## V52.9.148 — JEMIPAL / itinéraire unique
Branding JEMIPAL intégré. Fantôme READY neutralisé à la racine : séparation état logique / état visuel, un seul panneau Préparer+Résultats.


## V52.9.149 — paysage itinéraire unique
Portrait V148 gelé. Autorité CSS paysage ajoutée pour supprimer les grilles historiques concurrentes et contraindre Préparer + résultat à une seule feuille en deux lignes maximum. Moteur/GPS/caméra inchangés.


## V52.9.151 — READY libéré / actions flottantes
Paysage uniquement : préparation masquée après calcul ; résultats compacts ; Modifier/Démarrer flottants hors cadre. Portrait et chaîne GPS/routage/caméra inchangés.


## V52.9.155 — Nettoyage READY
Cause racine : data-state reste prepare en logique READY; anciennes règles data-route-phase maintenaient Préparer visible. Autorité finale ajoutée : READY seul dans les deux orientations.

## V52.9.155 — nettoyage démarrage accueil / anti-fenêtres fantômes
- Cause identifiée : `ar-mobile-home-open` n'était ajouté qu'au `window.load`; avant cet événement le navigateur pouvait peindre brièvement l'ancienne interface et/ou le lanceur historique.
- Correction : l'état accueil est maintenant présent directement sur `<body>` dès le parsing HTML.
- Ajout d'un garde de démarrage mobile qui masque toute brique hors accueil avant même l'initialisation JavaScript.
- Aucun changement GPS, géocodage, routage, caméra, conduite ou ruban métrique.

## V52.9.155 — démarrage direct accueil, suppression interstitiel historique
- Cause racine du flash restant : `profile-launcher` existait visible dans le HTML et le vieux bloc V50.2 le ré-ouvrait explicitement au `window.load` avant/pendant l'initialisation de l'accueil.
- Le sélecteur historique est maintenant `hidden` par défaut et V50.2 le maintient fermé au démarrage.
- Ajout d'une autorité de premier rendu sur `<html class="jepalys-boot-home">` : avant stabilisation de l'accueil, aucun autre enfant direct du body ne peut être peint.
- La classe de boot n'est retirée qu'après deux `requestAnimationFrame`, une fois l'accueil établi.
- V154 avait volontairement gelé les vues Préparer / Itinéraire prêt : aucune modification de leur logique dans V155.
- GPS, géocodage, routage, caméra et ruban métrique inchangés.


## V52.9.171 — reprise saine depuis V155
Nettoyage chirurgical des seules autorités visuelles itinéraire. Démarrage V155 conservé intact. À tester WP35.


## V52.9.173 — Sélection véhicule directe
- Base stricte V172.
- Accueil : clic véhicule disponible = sélection + ouverture automatique étape suivante.
- Bouton « Préparer un trajet » masqué/supprimé du parcours visuel.
- GPS/routage/carte/caméra/conduite et PREPARE/READY inchangés.
- Statut : à tester WP35.

## V52.9.174 — Véhicule connu : préparation directe
- Base stricte : V52.9.173 validée sur WP35.
- Une seule évolution ergonomique : pour Utilitaire / Camping-car / Bus / Poids lourd, si un véhicule enregistré est déjà actif/par défaut, son gabarit est appliqué automatiquement et JEPALYS ouvre directement la préparation d’itinéraire.
- L’écran complet « Quel véhicule conduisez-vous ? » reste accessible depuis « Gérer mes véhicules » / « Ajouter un véhicule » et reste obligatoire si aucun véhicule fiable n’est enregistré.
- Aucun changement GPS, routage, carte, caméra, PREPARE/READY ou conduite.
- Statut : à tester sur WP35.


## V52.9.175 — 2026-09-11
Gabarit commun compact pour les deux états Préparer / Prêt, base V174. Saut véhicule connu conservé. À tester WP35 portrait/paysage.

## V52.9.176 — 2026-09-11
- Base stricte V175.
- Véhicule sélectionné rendu plus visible à l’accueil et dans Préparer.
- Ajout de « Tournée » pour le profil Bus, branché sur les tournées déjà sauvegardées par l’API ; sélection = reprise Départ/Arrivée, puis calcul volontaire par le conducteur.
- Panneau Itinéraire prêt paysage recomposé dans un seul gabarit compact.
- GPS, géocodage, routage, carte, caméra et conduite non modifiés.
- Statut : à tester WP35 portrait/paysage après batterie complète.
- Contrôle automatisé V176 : 5/5 tests V176 verts ; syntaxe JS du bloc mobile vérifiée par Node ; frontends miroir identiques.
- Batterie historique comparative : V175 d'origine = 309 verts / 31 échecs historiques (hors blocage de collecte dû au lanceur V52.9.102 absent). V176 = 314 verts / les mêmes 31 échecs historiques. Aucun nouvel échec introduit par V176.


## V52.9.177 — Accueil identification + tournée
- « ACTIF » retiré : le cerclage vert suffit.
- Identification / n° de parc affiché dans la barre « Mon véhicule sélectionné ».
- En Bus, Tournée apparaît à côté de « Bus ».
- Nom long : défilement horizontal dans une zone fixe, sans modifier le format.
- GPS / routage / conduite : inchangés.


## V52.9.178 — 11/09/2026
- Accueil Bus, portrait : bulle Tournée affinée (17 px) et étendue sur la largeur disponible (max 66 %).
- Défilement des noms longs conservé.
- Paysage, GPS, routage et conduite non modifiés.

## V52.9.180 — 11/09/2026
- Correction immédiate de la régression V179 : boucle MutationObserver supprimée.
- Navigation accueil, liens et responsive portrait/paysage rétablis.
- La zone « Mon véhicule sélectionné » ouvre désormais la fiche de caractéristiques du véhicule actif.
- GPS/routage/conduite inchangés.


## V52.9.181
Clavier Android intégré aux formulaires : pas de barre flottante doublon, validation par touche Entrée/✓, identification véhicule persistée et répercutée immédiatement sur l’accueil.

## 2026-09-11 — V52.9.182 : barres Android intégrées
- Décision terrain : ne plus lutter contre les barres Android. Elles restent visibles et la coque se dimensionne dans la zone utile réellement disponible.
- Mode PWA principal passé de fullscreen à standalone.
- Les resize de même orientation dus à la zone système sont désormais acceptés ; le clavier reste géré séparément par V181.
- Pastille ID accueil légèrement élargie.

## 2026-09-11 — V52.9.182 : accueil adaptatif selon le profil
- Bloc « Mon véhicule sélectionné » visible uniquement pour Voiture, Utilitaire, Camping-car, Bus et Poids lourd.
- Piéton, Vélo et Moto utilisent une composition sans bloc véhicule, rééquilibrée en portrait et paysage.
- Barres Android intégrées à la zone utile et pastille ID élargie.
- Étape suivante après validation : fusion des deux fenêtres convenues.


## Correctif lanceur V182
- Le lanceur ne modifie plus `settings global policy_control` : diagnostic Android en lecture seule uniquement.
- Fichier BAT réécrit sans BOM UTF-8 pour garantir `@echo off` sous Windows CMD.
- Aucun changement GPS, routage, carte ou conduite.

## V52.9.183 — 11/09/2026
- Fenêtre de saisie flottante synchronisée avec le clavier Android en portrait et paysage.
- Validation conservée sur la touche Entrée/✓ du clavier natif.
- Stabilisation de la surface utile Android par orientation : une disparition des barres ne réagrandit plus la maquette.
- Aucun réglage Android global modifié par le lanceur.

## V52.9.184
Cadre Android réservé de façon stable par orientation, bulle clavier uniquement quand le clavier est ouvert, finition accueil/garage paysage. GPS/routage/conduite inchangés.

## V52.9.185 — cadre fixe / saisie visible
- Autorité finale de géométrie basée sur la plus petite visualViewport hors clavier par orientation.
- Réserve basse Android renforcée.
- Plein écran navigateur neutralisé pour éviter les variations des barres système.
- Bulle de saisie forcée au-dessus du clavier en portrait et paysage.

## V52.9.186
Viewport stable sans réserve Android artificielle. Saisie universelle flottante au-dessus du clavier en portrait/paysage. Accueil paysage resserré. GPS/routage/conduite inchangés.


## V52.9.187 — accueil compact + accordéon
- Accueil : vignettes et espacements légèrement réduits pour récupérer la partie basse.
- Gérer mes véhicules : Tournées / Identification / Caractéristiques deviennent trois rubriques repliables, une seule ouverte à la fois.
- Tester portrait + paysage, puis clavier sur chaque rubrique.

## 2026-09-11 — V52.9.188 « VIRAGE SERRÉ » — branche expérimentale à tester
- Branche Git créée : `virage-serre`, issue de la base V187.
- Objectif volontairement radical : ne conserver que deux vues utilisateur principales, **Accueil** et **Conduite**.
- Accueil : sélection du profil, véhicule, ID/caractéristiques/sauvegarde, tournées et préparation d'itinéraire réunis sur la même vue.
- L'ancienne page « Gérer mes véhicules » n'est plus utilisée par le nouveau parcours : la gestion véhicule passe par un menu et des fenêtres flottantes.
- Les profils ne quittent plus automatiquement l'accueil au clic ; le clic vaut sélection et met à jour le contexte.
- Le calcul d'itinéraire réutilise le moteur existant en arrière-plan ; « Démarrer » bascule ensuite sur la conduite existante afin de ne pas réécrire GPS/routage/conduite.
- Une démo sans GPS reste disponible depuis l'accueil.
- Statut : **à tester par moi**. Aucun commit de la V188 avant validation client.

## V52.9.189 — Virage serré validation
Accueil stabilisé comme centre de préparation. Petite bulle Tournée supprimée ; petit ID devient indicateur. Les deux grandes commandes ID véhicule / Mes tournées deviennent les seuls accès de gestion. Bouton itinéraire = Démarrer et bascule automatique vers Conduite après calcul. Paysage : bandeau JEPALYS réduit. Portrait : sous-titre redondant supprimé.


## V52.9.194 — corrections ciblées Virage serré
- Boutons ID véhicule et Mes tournées transformés en vrais menus déroulants ancrés sur l’accueil.
- Suppression du petit indicateur ID dans la fiche véhicule.
- Slogan « Explorer aujourd’hui, préserver demain. » rétabli dans le header, sans « Quel véhicule ? » ni phrase d’aide.
- Paysage rééquilibré (header, grille profils, colonne métier).
- Tournées gérées dans le menu déroulant, plus en fenêtre modale centrale.
- Calcul d’itinéraire masqué en arrière-plan : aucune vue « Préparer le trajet » affichée avant Conduite.


## V52.9.195 — Virage serré — finition saisie
Option A clavier validée : clavier Android natif conservé, saisie JEPALYS flottante au-dessus du clavier, menus paysage sur hauteur utile, doublon Tournée supprimé.

## Audit correctif V197 — 2026-09-12
- Cause principale de l'absence de clavier identifiée : le bloc V197 interceptait `pointerdown` avec `preventDefault()` puis focalisait une copie de champ en différé (`requestAnimationFrame`). Sur Android, cela pouvait casser le geste utilisateur autorisant l'ouverture de Gboard.
- Correction : retour au vrai champ HTML comme autorité unique de saisie. Aucun clone de champ, aucun `preventDefault()` sur les champs.
- Ajouter un véhicule / ID / caractéristiques / créer une tournée : focus du premier vrai champ conservé dans le geste utilisateur.
- Nettoyage automatique de tout état de saisie quand l'Accueil est quitté, pour empêcher une zone Destination de rester superposée à Conduite.
- Cadre profils corrigé : `grid-template-rows` explicites (et non `grid-auto-rows`) pour empêcher l'étirement vertical et les grands espaces entre les deux rangées en paysage.
- Aucun changement GPS, routage, carte ou logique Conduite.

## 2026-09-12 — V198 audit correctif (sans changement de version)
- Déclencheur : deux versions successives reproduisent le même défaut de saisie => application de la règle d'état des lieux correctif avant toute nouvelle version.
- Cause traitée : barre JEPALYS positionnée dynamiquement près du bas du visualViewport et interactions de focus trop fragiles après rotation/clavier.
- Correction : barre de saisie JEPALYS fixée dans la zone haute visible du viewport, focus renforcé dans le geste utilisateur, menu ancré et recalculé selon orientation, moins de réactions au scroll du visualViewport.
- Chronomètre Bus déplacé à droite, au-dessus du bouton ARRÊT, en portrait et paysage.
- Aucun changement GPS/routage/carte/caméra.

## Audit correctif V198 — focus natif + barres Android
- Réservation artificielle V184 neutralisée : JEPALYS utilise désormais uniquement le viewport réellement fourni par Android/Chrome, pour supprimer les grandes bandes noires.
- Saisie simplifiée : le champ réellement touché devient lui-même la zone de saisie flottante. Il reçoit directement le focus issu du geste utilisateur ; aucun second champ ne remplace le focus Android.
- Destination manuelle : désactivation de la tournée active maintenue au premier toucher.
- Menus ID/Tournées conservés, repositionnés après rotation.
- Chronomètre Bus inchangé dans cet audit.

## 2026-09-12 — V198 remise à plat Accueil
- Suppression des couches concurrentes Accueil/clavier depuis V180.
- Une seule autorité UI Accueil : panneaux inline, champs natifs, aucun clone/popup de saisie.
- Pas de visualViewport ni de réserve Android artificielle pour la saisie.
- Objectif : repartir d’une base simple avant toute nouvelle version.

## V52.9.199 — chantier complet Virage Serré — à tester par Jean-Paul
Remise en cohérence autour de deux vues visibles seulement (Accueil / Conduite), priorité absolue du vrai champ de saisie, suppression visuelle des vues legacy, navigation Conduite réduite au seul bouton Accueil, synchronisation tournée/itinéraire et Retour commercial, centrage des vignettes, priorité métier sur les encarts promotionnels, carte d'accueil recentrée et chrono Bus remonté en portrait.

## 2026-09-12 — V52.9.200 — Deux vues propres
- Nettoyage ciblé de la chaîne Accueil → calcul → Conduite.
- Suppression de l’ouverture visible du legacy Préparer pendant le calcul.
- Neutralisation des points d’entrée legacy et des états Prepare/Ready dans le parcours V1.
- Synchronisation tournée / Itinéraire / Retour commercial.

## V52.9.201
Ménage structurel : suppression des trois pages intermédiaires legacy, suppression de l’ancienne autorité clavier V52.9.51 et du gestionnaire tournées V179. Navigation recentrée sur Accueil ↔ Conduite.

## V52.9.202 — routage libre + saisie stabilisés
- Ménage préalable conservé : architecture visible limitée à Accueil + Conduite.
- Correction de la chaîne libre « Ma position → destination » : recherche GPS anticipée dès l’Accueil, réutilisation uniquement d’un fix GPS réellement frais et fiable déjà détenu par l’autorité GPS, puis calcul silencieux.
- Les erreurs du moteur de routage déclenchent désormais explicitement `allroads:route-error`, évitant un état Calcul figé.
- Fenêtre métier de saisie légèrement remontée et compactée ; vrai champ natif conservé visible.
- Hors tournée, modifier Destination remet toujours le départ à « Ma position ».

## V52.9.203 — finition panneaux Accueil
- Validation V202 : routage libre Ma position -> destination passe bien en Conduite.
- Finition : panneaux ID véhicule et Mes tournées ancrés de façon identique, plus haut, avec chevauchement volontaire d'environ la moitié des boutons d'appel.
- Saisie clavier : fenêtre métier prioritaire et remontée ; pas de modification du moteur/routage.

- V52.9.204 : finition Accueil — ancrage vertical des panneaux ID/Tournées + Itinéraire au premier plan pendant la saisie.

- V52.9.205 : finition Accueil — ancrage panneaux à mi-hauteur réelle, validation clavier Entrée, restauration saisie Itinéraire validée, hauteur clavier paysage sécurisée.

## V52.9.206 — validation explicite / boutons accessibles
- Destination : bouton Valider visible + Entrée Android reliée à la même validation.
- Panneaux ID/Tournées : rangée des boutons d’appel au-dessus du panneau afin de rester accessible.
- Piéton : fonctions véhicule retirées ; Vélo/Moto : fonctions pro légères.


## V52.9.207 — clavier JEPALYS plein écran
- Saisie native Android remplacée par une vue de saisie JEPALYS plein écran contrôlée par l’application.
- Validation explicite et fermeture par ×.


## V52.9.208 — 2026-09-12 — clavier JEPALYS : ouverture fiable
- Retour WP35 V207 : la fenêtre Modifier l’ID s’ouvrait mais aucun clavier JEPALYS n’apparaissait.
- Ménage ciblé dans la zone saisie : retrait des gestionnaires pointer/click dupliqués sur chaque input.
- Une seule délégation globale pilote désormais l’ouverture du clavier pour les champs présents et ceux créés dynamiquement dans les panneaux.
- Le mode de saisie d’origine est conservé avant `inputmode=none`, afin que les dimensions utilisent toujours le pavé numérique JEPALYS.
- GPS, routage, carte et Conduite inchangés. Statut : **à tester par moi** sur WP35, d’abord Modifier l’ID.


## V52.9.210 — 2026-09-12 — clavier JEPALYS : cause racine corrigée
- Contrôle avant correctif effectué sur J209.
- Cause racine : la garde Accueil masque tous les enfants directs de `body` hors `#allroads-mobile-home`; le clavier JEPALYS était justement injecté directement sous `body`, donc invisible et non tactile malgré son ouverture logique.
- Ménage : suppression du faux bouton transparent J209 et des déclencheurs concurrents.
- Autorité unique : clavier monté dans `#allroads-mobile-home` + une seule délégation de clic pour les champs/labels.
- Aucun changement GPS/routage/carte/Conduite. Statut : à tester WP35.


## V52.9.211 — 2026-09-12 — itinéraire réel visible dans la coque Conduite
- Retour WP35 : après Ma position → Feurs, la Conduite affichait encore 11,8 km / 15 min / 22:28.
- Audit : ces trois valeurs provenaient du HTML statique historique et n’étaient jamais raccordées au résultat du calcul réel.
- Correction propre : le HUD mobile prend désormais distance, durée et heure d’arrivée du calcul réel, puis les met à jour avec la progression GPS réelle.
- Instruction et distance de la prochaine manœuvre synchronisées avec le guidage GPS.
- Finition clavier : logo JEPALYS + fond plus translucide ; mécanisme de saisie J210 conservé.
- GPS, géocodage, moteur de routage, caméra et séparation Démo/Démarrer non réécrits.

## V52.9.212 — 2026-09-12 — cohérence 8 profils du banc développeur
- Audit avant correctif : les 8 profils étaient déverrouillés visuellement dans l’Accueil, mais l’API restait en état TEST par défaut.
- Cause exacte des 403 : `require_profile_access()` autorisait seulement Voiture + Bus, conformément au futur verrou commercial, tandis que l’interface annonçait « 8 profils accessibles ».
- Correction propre : le lanceur principal de développement pose explicitement `ALLROADS_ACCESS_STATE=PRO` et `ENVIRONMENT=development` avant de démarrer l’API.
- Le verrou commercial par défaut n’est pas affaibli : hors lanceur développeur, l’état TEST continue à n’autoriser que Voiture + Bus côté serveur.
- Aucun changement GPS, géocodage, routage, gabarit, carte, conduite ou clavier.

## V52.9.213 — 2026-09-12 — choix 3 itinéraires + préférences + coût véhicule actif
- Accueil conservé comme vue unique de préparation : comparaison de trois itinéraires (Recommandé / plus rapide / plus court) avant Conduite.
- Chaque choix affiche distance, durée, consommation et coût estimé selon le véhicule actif.
- Préférences persistantes et indépendantes : éviter autoroutes, éviter péages, éviter ferries.
- Règle figée : autoroute ≠ péage. Aucun péage n'est inventé par kilomètre ; sans donnée tarifaire réelle, affichage « à confirmer ».
- Profils hors phase test visuellement grisés « TEST INTERNE », mais toujours utilisables sur le banc développeur ; serveur TEST commercial inchangé (Voiture + Bus).
- Contrôles : 357 tests réussis, 53 historiques ignorés, JavaScript valide, miroirs frontend identiques.
- Statut : **à tester par moi** sur WP35.


## V52.9.214 — 2026-09-12 — clavier JEPALYS centre de choix itinéraire
- Accueil validé allégé : retrait des boutons Autoroute / Péage / Ferry de la carte Itinéraire.
- Destination : les préférences sont désormais intégrées à la fenêtre Saisie JEPALYS.
- Après validation de la destination, le même clavier compare et affiche jusqu'à 3 itinéraires avec km, durée, consommation et coût selon le véhicule actif.
- Un toucher sélectionne un itinéraire ; le bouton Valider devient Démarrer.
- Paysage : clavier à gauche et panneau préférences/itinéraires à droite ; portrait : panneau compact intégré au-dessus des touches.
- Autoroute, péage et ferry restent trois préférences indépendantes et mémorisées.
- Les profils de test internes restent grisés mais utilisables en mode développeur.
- Aucun changement de GPS, caméra ou logique de conduite. Statut : à tester sur WP35.
- Ajustement validé : en paysage, largeur du clavier ramenée à celle du portrait (~360–420 px) ; toute la largeur restante est réservée aux préférences et aux résultats km / temps / consommation / coût.


## V52.9.215 — 2026-09-12 — rapprochement Conduite calcul + géométrie
- J214 validée « grand luxe » conservée comme référence Accueil/clavier.
- Nettoyage : aucune seconde autorité caméra ajoutée ; `focusDrivingRoute()` reste le calculateur unique et `arE7ApplyDrivingCamera()` l’applicateur unique.
- Horizon caméra ramené à une enveloppe locale calculée : 45 s à la vitesse réelle, 180 m à 1,8 km, prochaine manœuvre bornée localement.
- Remplacement du balayage entier 11→17 par une résolution géométrique du facteur d’échelle depuis la route réellement projetée dans le rectangle sûr.
- Zoom Leaflet au quart de niveau (`zoomSnap=0.25`) ; aucun +1/+2 empirique.
- GPS, routage, ruban métrique, point conducteur 50/72 et J214 inchangés.
- Statut : **à tester WP35 en mouvement réel**.


## V52.9.216 — 2026-09-12 — tournée directe vers Conduite
- Correction après test WP35 : une tournée enregistrée est déjà un choix volontaire de trajet ; elle ne doit pas rouvrir la Saisie JEPALYS.
- Chargement Tournée ou Retour : activation des extrémités, calcul headless immédiat, puis Conduite automatique sur `allroads:route-ready`.
- Les préférences trajet mémorisées restent appliquées silencieusement.
- Clavier J214 et caméra géométrique J215 conservés sans modification fonctionnelle.
- Statut : à tester sur WP35.


## V52.9.217 — 2026-09-12 — carte Conduite visible / ARRÊT compact
- Base J216.
- Correction ciblée de la couche de fond qui pouvait rester vide en portrait après cadrage/orientation : invalidation de taille + redraw de la couche active après caméra et après stabilisation d’orientation.
- Géométrie caméra J215 inchangée.
- Bouton ARRÊT Bus flottant réduit de 72 px à 60 px pour libérer la zone basse.
- GPS, routage, tournées et clavier J214 inchangés.
- Statut : à tester sur WP35 portrait puis paysage.

## V52.9.218 — 2026-09-12 — niveau Conduite harmonisé portrait / paysage
- Base stricte J217 validée : affichage carte et bouton ARRÊT compact conservés.
- Caméra Conduite : même échelle métrique de départ dans les deux orientations, cible d'essai ~0,90 m/pixel (sensation voisine d'une vue ~200 m).
- À l'arrêt / très basse vitesse (<= 3 km/h), portrait et paysage utilisent exactement la même référence de zoom ; au-delà, le calcul géométrique dynamique J215 reprend.
- Une rotation d'écran en mouvement conserve brièvement le niveau déjà affiché afin d'éviter un saut de hauteur.
- Une perte momentanée de fraîcheur GPS pendant la rotation ne déclenche plus un fitBounds du trajet complet : le dernier cadrage déjà appliqué est maintenu, sans réutiliser une ancienne position GPS comme donnée métier.
- GPS, routage, itinéraire, gabarit et logique Conduite inchangés.
- Statut : à tester WP35 portrait puis paysage sur le même trajet.


## V52.9.219 — 2026-09-12 — borne basse caméra 3 m / 10 m
- Base J218 conservée.
- Borne haute : référence harmonisée ~200 m (0,90 m/pixel).
- Borne basse d’essai : caméra conceptuelle 3 m au-dessus / 10 m derrière, traduite géométriquement dans la carte 2D et plafonnée au zoom réel maximal 20.
- Les 10 m derrière déterminent le placement vertical du véhicule à partir des mètres/pixel réellement atteints.
- Entre les deux bornes, le calcul géométrique J215 reste l’autorité unique.
- Fond Leaflet clair neutralisé pendant rotation pour supprimer le voile blanc provenant de l’application.
- GPS, routage, tournée directe et clavier J214 inchangés. Statut : à tester WP35.


## V52.9.220 — caméra 1 m / 1 m + masque orientation
- Base J219 conservée.
- Borne basse expérimentale poussée de 3 m / 10 m à **1 m / 1 m**, sans grossissement CSS ; résolution limitée honnêtement par le zoom cartographique disponible.
- Point conducteur abaissé dans la zone utile en mode très basse vitesse pour traduire le recul de 1 m.
- Voile blanc portrait/paysage masqué par une surcouche sombre JEPALYS temporaire pendant la reconstruction de la carte.
- Borne haute ~200 m et calcul géométrique J215 entre les deux bornes conservés.
- GPS, routage, tournées, clavier et préférences trajet inchangés.
- Statut : **à tester par moi** sur WP35.


## V52.9.221 — prototype perspective Bus « assis sur le toit »
- Audit J220 avant correction : Leaflet 2D confirmé comme limite de la vue basse.
- Masque gris J220 supprimé.
- Prototype MapLibre GL isolé, Conduite Bus réelle uniquement, avec repli Leaflet automatique.
- Caméra physique provisoire : Bus 13 x 2,55 x 2,45 m, œil ~3,25 m, ~5,5 m derrière le centre GPS ramené sur route, regard ~45 m devant.
- GPS/routage/Accueil/tournées/alertes inchangés.
- Statut : à tester par moi sur WP35 portrait + paysage.


## V52.9.222 — rotation sans voile
- Contrôle J221 : le voile restant vient de la reconstruction du fond Leaflet pendant la rotation, pas du masque supprimé en 221.
- Nettoyage : aucun masque opaque ajouté.
- Correction : gel visuel du dernier rendu cartographique pendant la rotation, puis retrait après stabilisation du nouveau rendu.
- Désactivation des animations Leaflet de fondu/zoom pour éviter les états intermédiaires clairs.
- GPS/routage/tournées/Accueil/caméra géométrique inchangés.
- Statut : à tester sur WP35.


## V52.9.224 — stabilisation premier rendu Conduite
- Contrôle WP35 : ouverture portrait hors zone, paysage correct après rotation, retour portrait correct mais recadré.
- Nettoyage des rafraîchissements concurrents de rotation J222.
- Autorité unique `ar223StabilizeDrivingCamera` après stabilisation réelle de la coque, à l’entrée Conduite et après rotation.
- GPS, routage, tournées, Accueil J214 et logique métier inchangés.
- Statut : à tester sur WP35.


## V52.9.224 — test Voiture gabarit réel
- Base J223 conservée.
- Profil Voiture réglé sur L 4,40 m × l 1,80 m × H 1,50 m pour isoler l’effet du profil Bus dans une rue étroite/interdite aux bus.
- Aucun changement GPS, caméra, conduite, tournées ou moteur de routage.
- Statut : à tester sur WP35.


## V52.9.225 — restauration fond de carte après changement de profil
- Contrôle J224 : le fond sombre n'est pas un défaut GPS/routage ; une initialisation asynchrone du prototype perspective Bus pouvait réactiver son calque après passage en Voiture et masquer les panes Leaflet.
- Nettoyage : annulation par séquence et revalidation stricte du contexte Bus après chaque attente asynchrone.
- Voiture conserve le gabarit 4,40 × 1,80 × 1,50 m.
- GPS, itinéraire et caméra Leaflet inchangés.
- Statut : à tester WP35.


## V52.9.226 — nettoyage fantômes caméra / autorité unique
- Audit demandé sur J225 avant tout nouveau réglage de vue.
- Fantômes actifs/à risque isolés : prototype perspective J221, clone rotation J222, mode historique driver/overhead mémorisé, classes caméra anciennes.
- Nettoyage structurel : suppression des moteurs/masques concurrents et maintien d'une seule autorité Leaflet de cadrage.
- GPS, routage, tournée, gabarits et Accueil inchangés.
- Statut : à tester WP35 en Voiture, portrait puis paysage puis retour portrait.


## V52.9.227 — caméra métrique harmonisée portrait / paysage
- Contrôle WP35 : même position mais niveau de caméra différent selon l’orientation.
- Cause : zoom résolu à partir du rectangle pixel du viewport, donc portrait/paysage pouvaient diverger.
- Correction : niveau métrique commun indépendant de l’orientation ; même zoom Leaflet à position/vitesse/horizon identiques.
- Nettoyage : suppression des redraw() de tuiles dans la chaîne caméra afin d’éviter le fond sombre intermittent pendant les rotations.
- GPS, routage, tournées et Accueil inchangés. Statut : à tester par moi.


## V52.9.231 — reprise de route cohérente / mode test terrain réalisable
- Base volontaire : J227 propre.
- Les essais J229/J230 sont archivés comme expériences utiles, pas supprimés.
- Priorité visuelle fixée : tracé > véhicule > décor.
- Ruban : cœur métrique +5 % conservé, halo bleu sombre de contraste ajouté.
- Tracé remonté au premier plan après les mouvements caméra.
- Caméra terrain : ancre 74 %, horizon 50 s, minimum 280 m, portrait/paysage métriques cohérents.
- Aucune dépendance MapLibre/Cesium/3D payante dans cette branche.


## V52.9.232 — simulation sans GPS sur le vrai tracé
- Base : J231 test terrain, J227 conservé comme secours propre.
- Le bouton « Démo sans GPS » ne charge plus la route synthétique locale pour la simulation générique.
- La destination est d’abord résolue et le vrai itinéraire est calculé par le moteur existant.
- Après réception de `allroads:route-ready`, le GPS réel est arrêté et une position simulée progresse sur la géométrie `routeLayer`.
- La progression respecte la durée calculée (`duree_min`) et interpole la distance le long du vrai tracé.
- La position simulée devient une autorité explicite uniquement en mode simulation ; la conduite réelle reste strictement pilotée par le GPS frais fiable.
- La caméra, le ruban et les instructions réutilisent le même itinéraire que la conduite réelle.
- Les anciens scénarios synthétiques restent archivés dans le code mais ne sont plus lancés par le bouton générique « Démo sans GPS ».


## V52.9.233 — simulation GPS sur la carte réelle
- Diagnostic J232 confirmé sur WP35 : la position simulée avançait, mais `demoMode` forçait encore la couche synthétique.
- Nettoyage : séparation entre **source de position simulée** et **mode visuel de démonstration**.
- Nouveau drapeau `__allroadsRouteSimulationMode` : en simulation de trajet réel, la vue Conduite reste en mode cartographique `real`.
- Leaflet, le fond de carte, le ruban, la caméra et le véhicule restent les mêmes qu'en conduite GPS réelle ; seule la position est simulée le long du tracé calculé.
- L'ancienne scène synthétique est conservée dans le code historique mais n'est plus utilisée par `Démo sans GPS` depuis l'accueil Virage Serré.


## V52.9.234 — simulation GPS robuste + HUD anti-chevauchement
- Base : J233, sans toucher à J227 secours.
- Simulation sans GPS : durée recoupée entre donnée calculée, durée visible et géométrie réelle ; garde-fous physiques pour empêcher une fin instantanée.
- Position simulée : progression continue sur le vrai tracé, état diagnostic exposé dans `window.__allroadsRouteSimulationState`.
- HUD : recalage dynamique des commandes cartographiques et du compteur vitesse après resize/orientation afin d'éviter les chevauchements entre fenêtres flottantes.
- GPS réel, routage, accueil et clavier inchangés.


## J235 — nettoyage fantômes simulation
Audit avant implantation. Démo sans GPS est désormais un choix de source de position, pas un autre écran : clavier JEPALYS → comparaison → itinéraire réel → simulation sur routeLayer. Ancienne scène synthétique conservée uniquement comme archive non appelée.

## J237 — deux portes d’entrée, une seule application
- Base volontaire : J235, dernière simulation de route réelle validée avant l’expérience J236.
- Ajout d’une entrée partageable « Essais route » pour les chauffeurs testeurs : Bus + Voiture en phase TEST.
- Ajout d’une entrée personnelle « Accès interne » : accès complet aux 8 profils, réservé au propriétaire.
- Les deux entrées ouvrent exactement la même application ; aucun fork client n’est créé.
- Les droits sont contrôlés côté serveur par deux jetons distincts stockés en cookie HTTP-only après ouverture du lien.
- En local (PC/WP35 de développement), l’accès complet reste conservé automatiquement.
- Visuel « Essais route » validé ajouté aux ressources de la page d’entrée.
- GPS, routage, tournée, clavier JEPALYS, simulation J235 et caméra non modifiés.
- Statut : architecture prête à être publiée ; URL publique réelle à créer lors du déploiement Internet.

## J238 — Finition WP35/PWA accueil + conduite
- Base : J237 publiée, guidage/routage conservés sans modification.
- Portrait WP35 : logo légèrement rapproché de JEPALYS, slogan remonté, marge basse sûre.
- Paysage WP35 : compactage vertical ciblé pour rendre Itinéraire/Démarrer entièrement visibles.
- Conduite : le point bleu GPS Leaflet devient invisible ; le véhicule JEPALYS reste l'unique repère visuel.
- Conduite : indicateur GPS maintenu dans la barre haute afin d'éviter le chevauchement avec le véhicule.
- Service worker/cache porté à 52.9.238 pour forcer la prise en compte sur la PWA installée.


## J239 — contrôle terrain WP35 / conduite
- Référence : retour terrain J238 sur PWA WP35.
- Simulation sans GPS : mouvement continu par interpolation de distance sur le vrai tracé ; guidage et caméra cadencés séparément.
- Tracé conduite : cœur bleu + fin liseré blanc ; suppression du halo sombre/gris épais.
- Zoom paysage : les 3 commandes localisation / + / − restent visibles.
- Instructions : fenêtre manœuvre recalée ; texte contenu dans son champ ; ORS demandé en français + filet de normalisation UI.
- Barre système Android : thème clair afin de conserver les informations utiles (heure/réseau) visibles dans la PWA.
- Position : point GPS maintenu temporairement visible comme témoin de vérité ; véhicule placé dans le même pane visuel pour supprimer l'écart de transformation avant suppression définitive du point.
- Déploiement Render : buildCommand fixé sur api/requirements.txt.
