# Documentation du modèle de Machine Learning

## 1. Présentation du modèle

Le modèle utilisé a été développé et évalué lors du Projet 4. Il s'agit d'un modèle de **classification binaire basé sur une régression logistique**.

Les sorties sont les suivantes :

- `0` : le salarié reste dans l'entreprise.
- `1` : le salarié quitte l'entreprise.

Le modèle est intégré à une API développée avec FastAPI afin de rendre ses prédictions accessibles.

## 2. Algorithme utilisé

Le modèle retenu est une régression logistique (`LogisticRegression`).

Il évalue la probabilité qu'un salarié quitte l'entreprise en fonction de ses caractéristiques.

### Paramètres du modèle

Le modèle a été entraîné avec les paramètres suivants :

| Paramètre | Valeur | Rôle |
|---|---|---|
| `C` | `0.01` | Contrôle la régularisation du modèle |
| `class_weight` | `balanced` | Ajuste le poids des classes selon leur fréquence |
| `l1_ratio` | `0` | Définit la pondération de la régularisation L1/L2 |

## 3. Données utilisées

Le modèle se base sur 30 variables propres aux salariés.

Ces variables peuvent être regroupées en plusieurs catégories.

### Informations personnelles et professionnelles

- Âge
- Genre
- Situation matrimoniale
- Département
- Poste occupé
- Domaine d'étude
- Niveau d'éducation
- Nombre d'expériences précédentes
- Années d'expérience professionnelle totale

### Informations liées à l'entreprise

- Revenu mensuel
- Ancienneté dans l'entreprise
- Ancienneté dans le poste actuel
- Niveau hiérarchique du poste
- Nombre d'années auprès du responsable actuel
- Distance entre le domicile et le travail
- Fréquence des déplacements professionnels

### Satisfaction et évaluation

- Satisfaction concernant l'environnement de travail
- Satisfaction concernant la nature du travail
- Satisfaction concernant l'équipe
- Satisfaction concernant l'équilibre entre vie professionnelle et vie personnelle
- Note de l'évaluation précédente
- Note de l'évaluation actuelle

### Évolution professionnelle

- Heures supplémentaires
- Augmentation salariale précédente
- Nombre de participations au PEE
- Nombre de formations suivies
- Nombre d'années depuis la dernière promotion

### Variables calculées

Trois variables supplémentaires sont calculées :

- `ratio_anciennete_experience`
- `ratio_evolution_poste`
- `score_satisfaction_global`

## 4. Prétraitement des données

### Standardisation des variables numériques

Les variables numériques sont transformées à l'aide de `StandardScaler`.


### Encodage des variables catégorielles

Les variables catégorielles sont transformées à l'aide de `OneHotEncoder`.


Le paramètre `handle_unknown="ignore"` permet de gérer les catégories inconnues sans provoquer d'erreur lors de la transformation.

### Variables dérivées

L'API calcule trois variables avant d'effectuer la prédiction.

**1. Ratio ancienneté / expérience**

```python
ratio_anciennete_experience = (
    annees_dans_l_entreprise / annee_experience_totale
)
```

Si l'expérience totale est égale à zéro, le ratio est fixé à zéro afin d'éviter une division par zéro.

**2. Ratio évolution professionnelle**

```python
ratio_evolution_poste = (
    annees_depuis_la_derniere_promotion / annees_dans_l_entreprise
)
```

Si l'ancienneté est égale à zéro, le ratio est là encore fixé à zéro.

**3. Score de satisfaction global**

```python
score_satisfaction_global = moyenne(
    satisfaction_employee_environnement,
    satisfaction_employee_nature_travail,
    satisfaction_employee_equipe,
    satisfaction_employee_equilibre_pro_perso
)
```

## 5. Entraînement et sélection du modèle

Le modèle a été développé dans le cadre du Projet 4.

La sélection finale repose sur les résultats obtenus lors de la phase d'évaluation.

| Indicateur | Résultat |
|---|---|
| Precision | 0,321 |
| Recall | 0,766 |
| F1-score | 0,452 |

## 6. Intégration dans l'API

Le modèle entraîné est sauvegardé dans le fichier :

```text
app/model.joblib
```

Au démarrage de l'application, le modèle est chargé en mémoire :

```python
MODEL_PATH = Path(__file__).resolve().parent / "model.joblib"
model = joblib.load(MODEL_PATH)
```

## 7. Interprétation des résultats

Le modèle retourne une classe prédite ainsi que deux probabilités :

- `probabilite_depart` : probabilité estimée que le salarié quitte l'entreprise.
- `probabilite_rester` : probabilité estimée que le salarié reste dans l'entreprise.

L'API retourne également une interprétation textuelle :

- `Risque de départ élevé` lorsque la classe prédite est `1`.
- `Risque de départ faible` lorsque la classe prédite est `0`.

## 8. Limites et maintenance

Le modèle présente plusieurs limites :

- Ses prédictions dépendent de la qualité et de la représentativité des données d'entraînement.
- Les probabilités estimées ne garantissent pas qu'un salarié quittera effectivement l'entreprise.
- Les résultats peuvent être influencés par les variables utilisées lors de l'entraînement et par les éventuels biais présents dans les données.

Une future version pourrait intégrer un suivi des performances, une comparaison avec de nouveaux algorithmes et une surveillance de la qualité des prédictions.

---

**Projet :** OpenClassrooms - Projet 5  
**Application :** Futurisys ML API  
**Algorithme :** Régression logistique  
**Bibliothèque :** Scikit-learn