# API Itinéraire C25

API FastAPI de calcul et de gestion d’itinéraires.

## Installation

Depuis le dossier `api` :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Démarrage

Toujours lancer les commandes depuis `api` :

```powershell
python -m uvicorn main:app --reload
```

Documentation interactive : <http://127.0.0.1:8000/docs>

Routes principales :

- `GET /itineraire/calcul?lat1=48.8566&lon1=2.3522&lat2=49.4431&lon2=1.0993`
- `GET /itineraire/`

## Organisation

- `api/models/` contient les modèles SQLAlchemy, chacun défini une seule fois.
- `api/routers/` contient les routes FastAPI, sans redéfinition des modèles.
- `api/main.py` assemble l’application.

## Éviter la pollution Edge

- Ouvrir et modifier les fichiers Python dans VS Code, pas dans Edge.
- Retaper les commandes Uvicorn dans le terminal intégré VS Code.
- Vérifier tout fichier modifié avant de lancer l’API.
- Supprimer tout bloc inattendu tel que `edge_all_open_tabs` avant exécution.
- Utiliser Git pour repérer les modifications non souhaitées.


## V52.9.53 — test plein écran
Le WP35 peut maintenant demander le plein écran depuis l’interface avec `⛶ PLEIN ÉCRAN`, sans verrouiller l’orientation. Ce banc sert à valider l’espace réel avant la finition de l’accueil.

## V52.9.53
Saisie destination sécurisée au-dessus du clavier Android, stabilisation du viewport PWA WP35 et heartbeat obsolète rendu idempotent. La marge basse standard validée en V52.9.50 est conservée.

## Version V52.9.60
Consolidation WP35 : coque verticale figée entre rotations, retour du plein écran PWA prioritaire, header remonté au bord utile et ordre cartographique global Header → Carte/Relief/Satellite → guidage → carte. Validation terrain WP35 nécessaire pour confirmer la disparition des sauts liés aux barres Android.
