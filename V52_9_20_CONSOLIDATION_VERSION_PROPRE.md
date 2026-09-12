# AllRoad's V52.9.20 — consolidation version propre

- Empêche qu'un ancien serveur AllRoad's sur le port 8000 fasse tester une ancienne version sans s'en rendre compte.
- Lanceur affiche explicitement la version attendue et arrête uniquement un ancien processus uvicorn AllRoad's détecté sur le port 8000.
- Endpoint `/version` pour vérifier la version réellement servie.
- Désactivation du cache navigateur pour `/app` en développement.
- Correction de la purge des trajets automatiques avec SQLAlchemy `autoflush=False` (limite 20 réellement respectée).
- Test alertes rendu autonome : il crée sa donnée de test au lieu de dépendre d'une alerte ID 1 présente dans une base externe.
- Conservation des deux actions distinctes V52.9.19 : Recherche retournement / Signaler un blocage.
