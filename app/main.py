from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import joblib
import pandas as pd

app = FastAPI(
    title="Futurisys ML API",
    description="Projet 5 OCR - API de classification automatique basée sur le modèle du Projet 4.",
    version="1.1.0",
)

MODEL_PATH = Path(__file__).resolve().parent / "model.joblib"

model = joblib.load(MODEL_PATH)

class EmployeeData(BaseModel):

    # num
    age: float
    revenu_mensuel: float
    nombre_experiences_precedentes: float
    annee_experience_totale: float
    annees_dans_l_entreprise: float
    annees_dans_le_poste_actuel: float
    satisfaction_employee_environnement: float
    note_evaluation_precedente: float
    niveau_hierarchique_poste: float
    satisfaction_employee_nature_travail: float
    satisfaction_employee_equipe: float
    satisfaction_employee_equilibre_pro_perso: float
    note_evaluation_actuelle: float
    heure_supplementaires: float
    augementation_salaire_precedente: float
    nombre_participation_pee: float
    nb_formations_suivies: float
    distance_domicile_travail: float
    niveau_education: float
    annees_depuis_la_derniere_promotion: float
    annes_sous_responsable_actuel: float

    # cat
    genre: Literal["F", "M"]
    statut_marital: Literal["Célibataire", "Divorcé(e)", "Marié(e)"]
    departement: Literal[
        "Commercial",
        "Consulting",
        "Ressources Humaines"
    ]
    poste: Literal[
        "Assistant de Direction",
        "Cadre Commercial",
        "Consultant",
        "Directeur Technique",
        "Manager",
        "Représentant Commercial",
        "Ressources Humaines",
        "Senior Manager",
        "Tech Lead"
    ]
    domaine_etude: Literal[
        "Autre",
        "Entrepreunariat",
        "Infra & Cloud",
        "Marketing",
        "Ressources Humaines",
        "Transformation Digitale"
    ]
    frequence_deplacement: Literal[
        "Aucun",
        "Frequent",
        "Occasionnel"
    ]

@app.get("/")
def root():
    return {
        "message": "Acceuil de l'API pour Futurisys !",
        "status": "online",
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


@app.post("/predict")
def predict(employee: EmployeeData):

    input_data = pd.DataFrame([employee.model_dump()])

    input_data["ratio_anciennete_experience"] = (
        input_data["annees_dans_l_entreprise"]
        / input_data["annee_experience_totale"].replace(0, float("nan"))
    ).fillna(0)

    input_data["ratio_evolution_poste"] = (
        input_data["annees_depuis_la_derniere_promotion"]
        / input_data["annees_dans_l_entreprise"].replace(0, float("nan"))
    ).fillna(0)

    input_data["score_satisfaction_global"] = input_data[[
        "satisfaction_employee_environnement",
        "satisfaction_employee_nature_travail",
        "satisfaction_employee_equipe",
        "satisfaction_employee_equilibre_pro_perso"
    ]].mean(axis=1)

    input_data = input_data[model.feature_names_in_]
    prediction = int(model.predict(input_data)[0])
    proba = model.predict_proba(input_data)[0]
    proba_depart = float(proba[1])

    return {
        "prediction": prediction,
        "resultat": (
            "Risque de départ élevé"
            if prediction == 1
            else "Risque de départ faible"
        ),
        "probabilite_depart": round(proba_depart, 4),
        "probabilite_rester": round(float(proba[0]), 4)
    }