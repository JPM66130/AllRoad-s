# V52.9.201 — Architecture 2 vues propre

## Objectif
Supprimer les trois pages intermédiaires de l’expérience V1 : sélection véhicule legacy, Préparer le trajet, Itinéraire prêt.

## Nettoyage réalisé
- page legacy `#ar52-vehicle` supprimée avec son style et son contrôleur ;
- panneaux visuels `prepare` et `ready` supprimés du DOM ;
- ancienne barre globale clavier V52.9.51 supprimée ;
- ancien gestionnaire tournées V179 supprimé ;
- styles devenus exclusivement liés aux vues Prepare/Ready supprimés ;
- état moteur minimal conservé sous forme de champs cachés pour ne pas casser le moteur de calcul existant ;
- `AllRoadsMobileNav.open()` est désormais un adaptateur moteur qui reste sur Accueil ;
- `smartBack()` et les commandes historiques renvoient vers Accueil, jamais vers une page intermédiaire.

## Architecture visible
1. Accueil : profil, véhicule, tournées, départ/destination, calcul silencieux.
2. Conduite : carte, guidage, alertes, actions métier.

## Règles tournées
- tournée active = départ/destination sauvegardés ;
- Retour inverse départ/destination + arrêts + route ;
- modification manuelle de Destination désactive la tournée et remet le départ à `Ma position`.

## Important
Les champs cachés `ar51-from`, `ar51-to`, `ar51-km`, `ar51-min` ne sont pas des pages : ce sont des adaptateurs temporaires vers le moteur historique. Ils pourront être supprimés dans une étape ultérieure après extraction du moteur de routage dans un module autonome.
