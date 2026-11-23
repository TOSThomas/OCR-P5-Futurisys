<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://upload.wikimedia.org/wikipedia/fr/0/0d/Logo_OpenClassrooms.png?utm_source=fr.wikipedia.org&utm_campaign=imageinfo&utm_content=thumbnail_unscaled" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">OCR Projet 5 - Futurisys</h3>
  <p align="center">
    Déploiement d'une API de prédiction du risque de départ
    <br />
    <a href="https://github.com/TOSThomas/OCR-P5-Futurisys"><strong>Explore »</strong>
  </p>
</div>

## Présentation

Futurisys est une API de Machine Learning développée
avec FastAPI permettant de prédire le risque de départ
d'un salarié à partir de ses caractéristiques personnelles
et professionnelles.

Le projet repose sur un modèle de régression logistique
entraîné lors du Projet 4 et réutilisé dans cette API.

## Technologies utilisées

* [![Python][Python]][Python-url]
* [![uv][uv]][uv-url]
* [![FastAPI][FastAPI]][FastAPI-url]
* [![Scikit-learn][Scikit-learn]][Scikit-learn-url]
* [![Pandas][Pandas]][Pandas-url]
* [![Pydantic][Pydantic]][Pydantic-url]
* [![SQLAlchemy][SQLAlchemy]][SQLAlchemy-url]
* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
* [![Joblib][Joblib]][Joblib-url]
* [![Pytest][Pytest]][Pytest-url]

## Architecture du projet

```text
projet/
├── app/
│   ├── main.py
│   ├── bdd.py
│   ├── preprocessing.py
│   └── model.joblib
├── tests/
│   ├── test_main.py
│   └── test_preprocessing.py
├── docs/
│   ├── documentation_api.md
│   └── documentation_modele.md
├── .env.exemple
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

## Installation

Cloner le projet :

```bash
git clone https://github.com/TOSThomas/OCR-P5-Futurisys.git
cd futurisys
```

Installer les dépendances :
```
uv sync --locked
```

## Configuration du .env

Créer le fichier `.env` à la racine du projet.
Compléter le fichier à l'aide du `.env.exemple`.

Une instance PostgreSQL doit être accessible.

## Lancement de l'application

Démarrer l'API :

```bash
uv run uvicorn app.main:app --reload
```

L'API est accessible à l'adresse :

http://127.0.0.1:8000

## Documentation de l'API

Swagger :
http://127.0.0.1:8000/docs

ReDoc :
http://127.0.0.1:8000/redoc

## Endpoints disponibles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Accueil |
| GET | /health | État de l'API |
| POST | /predict | Prédiction du risque de départ |

## Exemple d'utilisation

Envoyer une requête POST sur `/predict`
avec les caractéristiques d'un salarié au format JSON.

L'API retourne :

- L'identifiant de la prédiction.
- La classe prédite.
- L'interprétation du résultat.
- La probabilité de départ.
- La probabilité de rester.

## Tests

Exécuter l'ensemble des tests :

```bash
uv run python -m pytest -v
```

Générer un rapport de couverture :

```bash
uv run python -m pytest --cov=app --cov-report=term-missing
```

Générer un rapport HTML :

```bash
uv run python -m pytest --cov=app --cov-report=html
```

## Documentation technique

`docs/documentation_api.md`  
`docs/documentation_modele.md`

[uv]: https://img.shields.io/badge/uv-DE5FE9?style=for-the-badge&logo=uv&logoColor=white
[uv-url]: https://docs.astral.sh/uv/

[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/

[FastAPI]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/

[Scikit-learn]: https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white
[Scikit-learn-url]: https://scikit-learn.org/

[Pandas]: https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/

[Pydantic]: https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white
[Pydantic-url]: https://docs.pydantic.dev/

[SQLAlchemy]: https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white
[SQLAlchemy-url]: https://www.sqlalchemy.org/

[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/

[Joblib]: https://img.shields.io/badge/Joblib-333333?style=for-the-badge&logo=python&logoColor=white
[Joblib-url]: https://joblib.readthedocs.io/

[Pytest]: https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white
[Pytest-url]: https://docs.pytest.org/