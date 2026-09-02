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
