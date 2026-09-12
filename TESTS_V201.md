# Tests V52.9.201

- JavaScript inline : 23 scripts contrôlés par `node --check`, 0 erreur.
- Suite pytest : 318 tests actifs réussis, 0 échec.
- 49 assertions historiques explicitement retirées du contrat actif : elles validaient les anciennes pages Prepare/Ready/Garage, d'anciens numéros de build ou d'anciens choix PWA. Elles restent présentes et sont marquées `skip` avec motif V201.
- Smoke test serveur : `/version` = V52.9.102 (moteur stable), `/app/?v=52.9.201` = HTTP 200.
- Frontends `frontend/index.html` et `api/frontend/index.html` : identiques.

## Contrat V201 contrôlé
- 2 vues utilisateur : Accueil + Conduite.
- aucune page `#ar52-vehicle`.
- aucun panneau visuel `data-panel="prepare"` ou `data-panel="ready"`.
- calcul route en mode headless depuis Accueil puis démarrage direct Conduite.
- modification manuelle de Destination : tournée désactivée + départ remis à `Ma position`.
- tournée aller/retour : inversion départ/destination + arrêts + route.
- ancienne autorité clavier V52.9.51 supprimée ; une seule autorité de saisie V198/V201.
