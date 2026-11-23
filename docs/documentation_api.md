# Documentation de l'API Futurisys

## 1. Présentation

L'API Futurisys permet d'interroger un modèle de Machine Learning afin d'estimer le risque de départ d'un salarié.

Elle a été développée avec FastAPI et utilise le modèle de classification entraîné lors du Projet 4.

L'API reçoit les informations d'un salarié au format JSON, effectue les traitements nécessaires, puis retourne une prédiction accompagnée de probabilités.

Les résultats sont également enregistrés dans une base de données PostgreSQL afin de conserver un historique des prédictions.

## 2. Installation et lancement

### Prérequis

- Python 3.12
- uv
- PostgreSQL
- Les dépendances du projet

### Installation des dépendances

Depuis le dossier racine du projet :

```bash
uv sync --locked
```

### Configuration de la base de données

Créer un fichier `.env` à la racine du projet à partir du fichier `.env.exemple`.

Renseigner les informations de connexion PostgreSQL :

```dotenv
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432
DB_NAME=futurisys
```

La base de données doit être accessible avec les identifiants renseignés.

### Initialisation de la base de données

```bash
uv run python -c "from app.bdd import setup_database; setup_database()"
```

Cette opération nécessite les droits PostgreSQL nécessaires à la création de la base si celle-ci n'existe pas encore.

### Démarrage de l'API

```bash
uv run uvicorn app.main:app --reload
```

Par défaut, l'API est accessible à l'adresse :

```text
http://127.0.0.1:8000
```

## 3. Documentation interactive

- Swagger UI : `http://127.0.0.1:8000/docs`
- ReDoc : `http://127.0.0.1:8000/redoc`

## 4. Endpoints disponibles

L'API expose trois endpoints principaux.

| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/` | Vérifie que l'API est accessible |
| GET | `/health` | Vérifie l'état de fonctionnement de l'API |
| POST | `/predict` | Effectue une prédiction du risque de départ |

### 4.1 Accueil de l'API

**Endpoint :** `GET /`

Permet de vérifier que l'API est accessible.

Exemple de réponse :

```json
{
  "message": "Acceuil de l'API pour Futurisys !",
  "status": "online"
}
```

**Code HTTP :** `200 OK`

### 4.2 Vérification de l'état de santé

**Endpoint :** `GET /health`

Permet de vérifier que l'application est opérationnelle.

Exemple de réponse :

```json
{
  "status": "healthy"
}
```

**Code HTTP :** `200 OK`

### 4.3. Prédiction du risque de départ

**Endpoint :** `POST /predict`

Cet endpoint constitue la fonctionnalité principale de l'API.

Il reçoit les données d'un salarié au format JSON, les valide, effectue les calculs nécessaires et transmet les données au modèle de Machine Learning.

La réponse contient la classe prédite, une interprétation textuelle et les probabilités estimées.

L'API attend 27 variables en entrée.

**Variables numériques :**

| Champ | Type | Description |
|---|---|---|
| `age` | Nombre | Âge du salarié |
| `revenu_mensuel` | Nombre | Revenu mensuel |
| `nombre_experiences_precedentes` | Nombre | Nombre d'expériences précédentes |
| `annee_experience_totale` | Nombre | Expérience professionnelle totale |
| `annees_dans_l_entreprise` | Nombre | Ancienneté dans l'entreprise |
| `annees_dans_le_poste_actuel` | Nombre | Ancienneté dans le poste actuel |
| `satisfaction_employee_environnement` | Nombre | Satisfaction concernant l'environnement |
| `note_evaluation_precedente` | Nombre | Note de l'évaluation précédente |
| `niveau_hierarchique_poste` | Nombre | Niveau hiérarchique |
| `satisfaction_employee_nature_travail` | Nombre | Satisfaction concernant le travail |
| `satisfaction_employee_equipe` | Nombre | Satisfaction concernant l'équipe |
| `satisfaction_employee_equilibre_pro_perso` | Nombre | Satisfaction concernant l'équilibre professionnel/personnel |
| `note_evaluation_actuelle` | Nombre | Note de l'évaluation actuelle |
| `heure_supplementaires` | Nombre | Indicateur d'heures supplémentaires |
| `augementation_salaire_precedente` | Nombre | Augmentation salariale précédente |
| `nombre_participation_pee` | Nombre | Nombre de participations au PEE |
| `nb_formations_suivies` | Nombre | Nombre de formations suivies |
| `distance_domicile_travail` | Nombre | Distance domicile-travail |
| `niveau_education` | Nombre | Niveau d'éducation |
| `annees_depuis_la_derniere_promotion` | Nombre | Années depuis la dernière promotion |
| `annes_sous_responsable_actuel` | Nombre | Années auprès du responsable actuel |

**Variables catégorielles :**

| Champ | Valeurs autorisées |
|---|---|
| `genre` | `F`, `M` |
| `statut_marital` | `Célibataire`, `Divorcé(e)`, `Marié(e)` |
| `departement` | `Commercial`, `Consulting`, `Ressources Humaines` |
| `poste` | `Assistant de Direction`, `Cadre Commercial`, `Consultant`, `Directeur Technique`, `Manager`, `Représentant Commercial`, `Ressources Humaines`, `Senior Manager`, `Tech Lead` |
| `domaine_etude` | `Autre`, `Entrepreunariat`, `Infra & Cloud`, `Marketing`, `Ressources Humaines`, `Transformation Digitale` |
| `frequence_deplacement` | `Aucun`, `Frequent`, `Occasionnel` |

#### Exemple de requête JSON

```json
{
  "age": 35,
  "revenu_mensuel": 5000,
  "nombre_experiences_precedentes": 2,
  "annee_experience_totale": 10,
  "annees_dans_l_entreprise": 5,
  "annees_dans_le_poste_actuel": 3,
  "satisfaction_employee_environnement": 3,
  "note_evaluation_precedente": 3,
  "niveau_hierarchique_poste": 2,
  "satisfaction_employee_nature_travail": 3,
  "satisfaction_employee_equipe": 3,
  "satisfaction_employee_equilibre_pro_perso": 3,
  "note_evaluation_actuelle": 3,
  "heure_supplementaires": 0,
  "augementation_salaire_precedente": 15,
  "nombre_participation_pee": 1,
  "nb_formations_suivies": 3,
  "distance_domicile_travail": 10,
  "niveau_education": 3,
  "domaine_etude": "Infra & Cloud",
  "frequence_deplacement": "Occasionnel",
  "annees_depuis_la_derniere_promotion": 1,
  "annes_sous_responsable_actuel": 2,
  "genre": "M",
  "statut_marital": "Marié(e)",
  "departement": "Consulting",
  "poste": "Consultant"
}
```

#### Exemple de réponse

```json
{
  "id_prediction": 17,
  "prediction": 0,
  "resultat": "Risque de départ faible",
  "probabilite_depart": 0.2746,
  "probabilite_rester": 0.7254
}
```

#### Description des champs retournés

| Champ | Type | Description |
|---|---|---|
| `id_prediction` | Entier | Identifiant de la prédiction enregistrée en base |
| `prediction` | Entier | Classe prédite : `0` ou `1` |
| `resultat` | Texte | Interprétation de la classe prédite |
| `probabilite_depart` | Nombre | Probabilité estimée de départ |
| `probabilite_rester` | Nombre | Probabilité estimée de non départ |

Les probabilités sont comprises entre 0 et 1 et leur somme est égale à 1, à l'arrondi près.

#### Codes HTTP

| Code | Signification |
|---|---|
| `200 OK` | Prédiction effectuée avec succès |
| `422 Unprocessable Entity` | Données manquantes, invalides ou incompatibles avec le schéma attendu |
| `500 Internal Server Error` | Erreur interne lors du traitement de la requête |

## 5. Stockage des prédictions

Chaque prédiction effectuée est enregistrée dans la base PostgreSQL, dans la table `predictions`. Elle conserve :

- Un identifiant unique.
- La date et l'heure de la prédiction.
- La classe prédite.
- La probabilité de départ.
- La probabilité de maintien.
- Les données du salarié utilisées pour la prédiction, stockées au format JSON.

## 6. Sécurité et évolutions possibles

- Ajouter une authentification et une gestion des autorisations.
- Mettre en place une communication HTTPS.
- Limiter l'accès aux données personnelles.
- Encadrer la durée de conservation des données.
- Mettre en place une surveillance de la disponibilité de l'API et de la base de données.

Les données relatives aux salariés étant sensibles, leur traitement doit respecter les règles applicables en matière de protection des données personnelles.

---

**Projet :** OpenClassrooms - Projet 5  
**Application :** Futurisys ML API  
**Framework :** FastAPI