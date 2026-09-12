# Registre fonctionnel commercial AllRoad’s

| Fonction | Bénéfice | Profils | Mode conducteur | Statut |
|---|---|---|---|---|
| Rapport d’incident | Trace structurée d’un blocage et de sa résolution | Voiture, Utilitaire, Camping-car, Bus, Poids lourd | Collecte **Automatique** ; ouverture/validation **À la demande** ; commentaire **Intervention facultative** | **En validation** |
| Copie synthétique client/exploitant | Informer un destinataire autorisé sans ressaisie conducteur | Entreprise | Envoi **Automatique configurable** après validation | **Prévu** — aucun envoi externe en V52.9.35 |
| Recherche de retournement sûre | Proposer une zone atteignable en marche avant avant le blocage et compatible gabarit | Grands gabarits | Déclenchement **À la demande**, analyse **Automatique** | **Opérationnel / démo contrôlée** |
| Verrouillage pendant message important | Évite des transitions concurrentes pendant une confirmation | Tous profils actifs | **Automatique** | **Opérationnel** |
| Sélection persistante profil/véhicule | Évite l’ambiguïté sur le véhicule actif | Bus, Voiture actuellement actifs | **Automatique** après sélection | **Opérationnel** |
| Branding B2B | Personnalisation véhicule, bandeau ou les deux | Voiture, Utilitaire, Camping-car, Bus, Poids lourd | Aucun geste conducteur | **Prévu / architecture posée** |


## V52.9.39 — Standardisation industrielle interface
- Coque fonctionnelle standardisée hors accueil.
- Retour / Accueil : mêmes libellés et même emplacement.
- Barre conduite portrait équilibrée et retour discrètement souligné.
- Mode : automatique (interface). Statut : en validation WP35.

## V52.9.39 — Coque standard et branding extensible
- Navigation hors accueil : Retour — marque — Accueil — profil véhicule.
- Branding entreprise : architecture prévue, optionnelle, non activée par défaut.
- La zone centrale accepte une identité client sans déplacer les commandes standard.
- Statut : coque opérationnelle à valider WP35 ; branding client préparé, non commercialement activé.

## V52.9.42 — Paysage professionnel
- Accueil signature paysage : composition 4 × 2, visuels `cover`, texte superposé, proportions non tassées.
- Choix véhicule paysage : zones titre/contexte, liste, outils et validation figées dans le viewport visible.
- Préparation trajet paysage : panneau horizontal compact standardisé.
- `Itinéraire prêt` et `Conduite en cours` restent les références paysage validées, sans refonte dans cette version.
- Coque standard : `Retour — ALLROAD'S — Accueil — profil`.


### V52.9.53 — Plein écran / image produit
- Statut : banc de validation WP35.
- But : retirer visuellement les barres navigateur pendant la démonstration et mesurer l’espace réellement disponible.
- Orientation : conservée, jamais forcée.
- Aucun changement de logique métier ou sécurité.

### V52.9.53 — ergonomie clavier / stabilité PWA
- Champ de destination actif maintenu visible avec clavier Android : intégré, à valider WP35.
- Coque PWA : contrôleur de viewport principal unifié pour supprimer les oscillations concurrentes.
- Heartbeat statistique obsolète après redémarrage : réponse idempotente sans 404 parasite.
- Marge basse standard V52.9.50 : conservée comme référence validée.

### V52.9.53 — continuité conducteur / coque stable
- Itinéraire prêt : `Modifier` à gauche, `Démarrer` à droite pour continuité du geste.
- Sélection véhicule portrait : confirmation/CTA ancré en bas, sans grand vide sous le bouton principal.
- PWA installée : hauteur de coque figée entre rotations ; les micro-resize Android/scrcpy ne pilotent plus le layout.
- Marge basse standard V52.9.50 conservée.

### V52.9.53 — Mise à jour PWA et pont WP35
- Lanceur multi-cibles ADB : sélection explicite de la cible TCP/IP et `adb -s`.
- Mise à jour PWA : document principal, manifeste et service worker jamais servis depuis un ancien cache applicatif.
- Activation d'une nouvelle version : reprise automatique de la fenêtre PWA ouverte.
- Icône PWA conservée entre versions.

### V52.9.58 — finition panneau / stabilité PWA
- `Préparer le trajet` : fronton portrait compact aligné visuellement sur la famille `Itinéraire prêt`.
- Stabilité : suppression d'un rechargement différé possible du service worker et du polling du pont de banc en usage normal.
- Marge basse standard 6 px : inchangée.

### V52.9.58 — compactage véhicule / stabilité système Android
- Référence visuelle véhicule validée transposée au code.
- Gabarit permanent compact et sans chevauchement.
- Action principale bleue et hiérarchie AllRoad’s renforcée.
- Carte / Relief / Satellite figé entre coque et guidage.
- PWA en `standalone` pour stabiliser les barres système Android ; validation WP35 en cours.

### V52.9.60 — coque figée / structure cartographique de référence
- **Statut :** technique validé, validation WP35 requise.
- Abandon de la stratégie `standalone` V58 qui amplifiait les sauts d’écran.
- PWA `fullscreen` prioritaire avec `standalone` de repli.
- Une seule hauteur de coque entre deux rotations ; apparition/disparition des barres Android ignorée pour le layout AllRoad’s.
- Header remonté au bord utile du viewport avec marge fixe minimale.
- Ordre standard imposé aux vues cartographiques : Header → Carte/Relief/Satellite → guidage éventuel → carte.
- Écran véhicule compact V58 conservé comme référence validée.
