# AllRoads V52.4.2 — Pont simultané PC ↔ téléphone

Correction ciblée du mode test local :
- la console PC et AllRoads mobile peuvent rester ouverts en même temps ;
- le pont de test est volontairement non bloquant ;
- les requêtes du téléphone disposent d'un délai court et sont abandonnées silencieusement si le pont ne répond pas ;
- la synchronisation est espacée afin de ne jamais ralentir l'application ;
- la console PC interroge l'état moins fréquemment ;
- aucune commande du pont n'est nécessaire au fonctionnement normal d'AllRoads.

Le pont reste réservé au développement local.
