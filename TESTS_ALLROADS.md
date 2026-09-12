## V52.9.53 — plein écran corrigé

- Suite complète : 114 tests OK.
- Géographie : 9/9 OK.
- Navigation / chauffeur / données route : 3/3 OK.
- Python + JavaScript : syntaxe OK.
- ORS externe : SKIP si clé locale absente.
- Régression : le bouton plein écran reste visible sur l’accueil.

# Tests groupés AllRoads

## Bloc 1 — Navigation / Bus

Le fichier `tester_navigation.bat` lance en une fois le scénario principal chauffeur bus :

1. vérification du profil et des dimensions du bus ;
2. calcul d'un trajet bus ;
3. contrôle du plafond de vitesse à 90 km/h ;
4. nommage de la tournée ;
5. enregistrement d'un arrêt avec position et sens ;
6. récupération dans l'historique ;
7. mise à jour du compteur kilométrique.

Le moteur routier est simulé pendant ce test automatique. Cela évite un coût, une clé API ou une panne Internet, tout en vérifiant que les composants AllRoads communiquent correctement entre eux.

### Pour lancer le test sous Windows

Double-cliquer sur `tester_navigation.bat`.

Résultat attendu :

`1 passed`

puis :

`RESULTAT : OK - bloc Navigation / Bus valide.`

## Important — état actuel du profil bus

Les dimensions du véhicule sont mémorisées par AllRoads. Pour Bus, Utilitaire, Camping-car et Poids lourd, un moteur HGV compatible doit désormais confirmer le calcul avant que le guidage réel soit autorisé. Un secours automobile peut rester visible à titre informatif, mais le démarrage GPS est bloqué lorsque le gabarit n'est pas garanti. La validation terrain et la signalisation réelle restent obligatoires.

### V52.9.42 — contrôle paysage pro
- Suite pytest : 106 tests verts.
- Bloc navigation : vert.
- Vérification géographique : 9/9 verts.
- Compilation Python : OK.
- Syntaxe JavaScript embarquée : OK.
- Formulation interdite runtime `Revenez sur vos pas` : absente des fichiers produit.
- ORS externe : SKIP si clé locale absente.
- Contrôle à réaliser sur WP35 : Accueil, Choix véhicule, Préparer le trajet en paysage. `Itinéraire prêt` et `Conduite en cours` servent de références et ne doivent pas régresser.


## V52.9.53
- Contrôler activation plein écran sur geste utilisateur.
- Vérifier portrait puis paysage sans changement forcé d’orientation.
- Vérifier redimensionnement carte/panneaux après activation.
- Vérifier que les vues ready/driving restent inchangées fonctionnellement.

### Résultat technique V52.9.53
- Suite pytest complète : 113 tests verts.
- Bloc navigation : 1 test vert.
- Bloc fonctions chauffeur : 1 test vert.
- Bloc données route : 1 test vert.
- Vérification géographique : 9/9 verts.
- Compilation Python : OK.
- Syntaxe JavaScript embarquée : 9 scripts OK.
- Frontends racine/API : identiques.
- Version endpoint : V52.9.53.
- Contrôle runtime de la formulation interdite : OK.
- ORS externe : SKIP si clé locale absente.
- Validation restante : comportement réel du plein écran sur WP35, portrait et paysage.

## V52.9.53 — validation finale
- Suite complète : 136 tests verts.
- Navigation : 1/1 vert.
- Fonctions chauffeur : 1/1 vert.
- Données route : 1/1 vert.
- Géographie : 9/9 verts.
- Python compileall : OK.
- JavaScript inline : 13 scripts vérifiés avec `node --check` ; service worker : OK.
- Copies frontend + service worker : identiques.
- Phrase runtime interdite « Revenez sur vos pas » : absente.
- Heartbeat session obsolète : HTTP 200 idempotent validé.
- ORS externe : SKIP normal dans l'environnement de fabrication (clé non exposée).

## V52.9.53 — Continuité conducteur + stabilité PWA
- Suite pytest complète : 141 tests verts.
- Navigation : 1 test groupé vert.
- Chauffeur : 1 test groupé vert.
- Données route : 1 test groupé vert.
- Géographie : 9/9 verts.
- Compilation Python : OK.
- JavaScript : 13 scripts inline par copie + service worker vérifiés avec `node --check`.
- Frontend source / copie API identiques.
- Serveur smoke : `/version`, `/app/`, manifest, service worker et heartbeat obsolète en 200.
- Phrase runtime interdite « Revenez sur vos pas » absente.
- ORS smoke : SKIP normal en environnement sans clé.

## V52.9.53 — PWA / ADB fiable WP35
- Suite complète : 146 tests pytest passés.
- Blocs ciblés navigation / chauffeur / données route : 1/1 chacun.
- Géographie : 9/9 + banc `run_geo_check.py` OK.
- JavaScript : 12 scripts inline par frontend + service worker validés par `node --check`.
- Serveur local : `/version`, `/app/`, `sw.js`, `manifest.webmanifest` = HTTP 200.
- Cache HTTP des ressources `/app` : `no-store` confirmé.
- Régression corrigée pendant le cycle : anciens tests de nom de lanceur/cache mis à jour, puis suite complète relancée à zéro échec.

## V52.9.58 — panneau compact + stabilité différée
- Suite pytest complète : 150 verts.
- Navigation : 1/1 vert.
- Chauffeur : 1/1 vert.
- Données route : 1/1 vert.
- Géographie : 9/9 verts.
- JavaScript inline : 12 scripts syntaxiquement valides + service worker valide.
- Copies frontend : identiques.
- Régression dédiée : fronton portrait compact, pont de banc inactif en usage conducteur, aucune navigation forcée du service worker.

## V52.9.58 — référence compacte / standalone stable
- Vérifier la compacité portrait de la sélection véhicule et l'absence de chevauchement.
- Vérifier le CTA principal bleu et la fiche gabarit permanente.
- Vérifier Carte / Relief / Satellite entre coque et guidage.
- Vérifier manifest `display: standalone` et absence de `fullscreen` dans `display_override`.

## V52.9.60 — coque WP35 figée / ordre cartographique unique
- Suite pytest complète : 167 tests verts après correction des régressions V58 obsolètes.
- Navigation : 1/1 vert.
- Chauffeur : 1/1 vert.
- Données route : 1/1 vert.
- Géographie : 9/9 verts.
- Python compileall : OK.
- JavaScript inline : 14 scripts par frontend + service worker validés par `node --check`.
- Frontend source / copie API, manifeste et service worker : identiques.
- Serveur local : `/version`, `/app/`, manifest et service worker = HTTP 200.
- Régression V58 `standalone` rejetée : retour `fullscreen` prioritaire, `standalone` en repli.
- Coque : hauteur capturée au démarrage et recalcul uniquement lors d’une vraie rotation ; `visualViewport` reste dédié au clavier.
- Ordre cartographique : Header → Carte/Relief/Satellite → guidage → carte.

## V52.9.129
- 335 tests pytest : OK.
- Régression dédiée : facteur de couverture de rotation calculé, absence de `scale(1.18)`, compensation du centre et du zoom.
- 20 scripts inline par frontend + sw.js/app.js/allroads_ui_final.js : `node --check` OK.
- `api/frontend/index.html` et `frontend/index.html` identiques.


## V52.9.130
- Suite complète : 339 tests pytest verts.
- Régression dédiée : orientation/rafraîchissement ne change plus le fond en état Conduire.
