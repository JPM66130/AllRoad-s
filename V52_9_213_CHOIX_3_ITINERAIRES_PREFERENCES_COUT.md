# V52.9.213 — 3 itinéraires, préférences et coût véhicule actif

## Accueil validé : dernière brique itinéraire
- Après saisie Départ / Destination, JEPALYS compare trois stratégies : **Recommandé**, **Le plus rapide**, **Le plus court**.
- Chaque proposition affiche : kilomètres, durée, consommation estimée et coût estimé.
- La consommation utilise la consommation du **véhicule actif** ; changer de véhicule modifie donc l'estimation.

## Préférences conducteur mémorisées
Trois choix indépendants sont enregistrés localement :
- Sans autoroute ;
- Sans péage ;
- Sans ferry.

Autoroute et péage restent strictement distincts. Une autoroute gratuite ne génère aucun péage artificiel. Tant qu'une donnée tarifaire réelle de section n'est pas disponible, le péage est affiché **à confirmer** et n'est pas inventé dans le total.

## Profils phase de tests
- Voiture + Bus restent en affichage normal.
- Piéton, Vélo, Moto, Utilitaire, Camping-car et Poids lourd sont visuellement grisés avec la mention **TEST INTERNE**.
- Sur le banc développeur JEPALYS, ils restent cliquables et routables.
- Hors mode développeur, la sécurité serveur TEST conserve Voiture + Bus seulement.

## Architecture
- Toujours deux vues utilisateur : **Accueil ↔ Conduite**.
- Le choix des trois itinéraires est une surcouche de décision dans l'Accueil, pas une nouvelle page.
- GPS, caméra Conduite, alertes et clavier JEPALYS ne sont pas réécrits.

## Validation automatique
- Batterie complète : 357 tests réussis, 53 contrats historiques volontairement ignorés.
- 25 scripts JavaScript inline : syntaxe valide.
- Frontends `api/frontend/index.html` et `frontend/index.html` identiques.
