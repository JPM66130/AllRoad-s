# V52.9.237 — Double accès Essais route / Interne

Base : J235.

Objectif : une seule application avec deux portes d’entrée permanentes.

- Chauffeurs : `/essais-route/<jeton_testeur>` → droits TEST (Bus + Voiture).
- Jean-Paul : `/acces-interne/<jeton_proprietaire>` → accès complet aux 8 profils.
- Les liens restent indépendants du numéro de version de l’application.
- Les jetons sont validés côté serveur puis conservés en cookie HTTP-only.
- Le visuel public ne contient pas de mention JEPALYS/AllRoad’s.
- Le comportement navigation / GPS / simulation est celui de J235.
