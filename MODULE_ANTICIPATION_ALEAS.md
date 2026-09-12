# AllRoad's — Module d'anticipation des aléas

## Principe
Une seule couche métier consolide les aléas connus ou prévus sur l'itinéraire. Elle raisonne avec : position, itinéraire, sens de déplacement, profil/gabarit véhicule, heure estimée de passage, fiabilité et fraîcheur de la source.

## Familles prévues
- météo dangereuse : orage, rafales/vent latéral, neige, verglas, inondation, chaleur ;
- travaux, fermetures et restrictions temporaires programmées ;
- accidents, déviations et événements routiers lorsqu'une source fiable les fournit ;
- contraintes de gabarit, tonnage, largeur, hauteur, pente ou route étroite ;
- qualité GPS/réseau ;
- recherche d'une zone d'arrêt sûre et compatible avec le véhicule.

## Niveaux
1. Information anticipative.
2. Vigilance.
3. Danger / incompatibilité nécessitant une action.

Une prévision n'est jamais présentée comme un fait certain. Toute donnée doit conserver son niveau de confiance et son horodatage.

## Comportement cible
Avant départ : briefing « Trajet analysé » avec uniquement les aléas pertinents à l'heure estimée de passage.
En route : prévenir suffisamment tôt. Si une incompatibilité fiable compromet le trajet, recalculer/proposer une solution avant la zone, en respectant les règles fail-safe AllRoad's.

## Priorité de développement
Architecture réservée dans V52.9.81. L'alimentation temps réel ne doit pas être simulée comme réelle : elle sera branchée source par source après stabilisation de la version routière.
