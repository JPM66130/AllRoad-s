# V52.8.8 — Compteur statistique d'utilisation « aveugle »

## Objectif
Mesurer l'utilisation réelle d'AllRoad's sans enregistrer les déplacements.

## Déclenchement
- L'ouverture seule de l'application n'est pas comptée.
- Une session démarre au lancement de la navigation/conduite.
- Les écrans conduite, incident et retournement restent dans la même session.
- La session se termine lors du retour à la préparation/itinéraire prêt, à la fin de la simulation ou à la fermeture de la page.
- Une session n'est retenue dans les statistiques qu'à partir de 30 secondes d'activité.
- Les battements sont bornés pour qu'un onglet laissé ouvert ou un téléphone verrouillé ne gonfle pas artificiellement la durée.

## Données conservées
- identifiant pseudonymisé par hachage salé côté serveur ;
- profil : Piéton, Vélo, Moto, Voiture, Utilitaire, Camping-car, Bus, Poids lourd ;
- mode : navigation ou simulation ;
- dates de début / dernière activité / fin ;
- durée active cumulée.

## Données volontairement absentes
Aucune coordonnée GPS, aucun départ, aucune destination, aucun historique géographique, aucune adresse IP ni user-agent ne sont inscrits dans la table statistique.

## Exploitation
`GET /usage/stats?period=day|week|month`
retourne : utilisateurs actifs pseudonymisés, nombre de sessions, durée totale, moyenne par utilisateur actif, statistiques par profil et comparaison directe Bus / Voiture.

Cette architecture est conçue selon un principe de minimisation des données. La conformité RGPD finale dépendra aussi des mentions d'information, de la base légale, des durées de conservation et des procédures d'exploitation retenues lors du lancement.
