from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import joblib
import pandas as pd
import json
from app.bdd import SessionLocal, Prediction
from app.preprocessing import prepare_employee_data

app = FastAPI(
    title="Futurisys ML API",
    description="Projet 5 OCR - API de classification automatique basée sur le modèle du Projet 4.",
    version="1.3.0",
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
    
    input_data = prepare_employee_data(employee.model_dump())

    input_data = input_data[model.feature_names_in_]
    prediction = int(model.predict(input_data)[0])
    proba = model.predict_proba(input_data)[0]

    proba_depart = float(proba[1])
    proba_reste = float(proba[0])

    employee_data = json.loads(
        input_data.to_json(orient="records")
    )[0]
    db = SessionLocal()

    try:
        new_prediction = Prediction(
            prediction=prediction,
            probabilite_depart=proba_depart,
            probabilite_rester=proba_reste,
            donnees_salarie=employee_data
        )

        db.add(new_prediction)
        db.commit()
        db.refresh(new_prediction)
        prediction_id = new_prediction.id

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

    return {
        "id_prediction": prediction_id,
        "prediction": prediction,
        "resultat": (
            "Risque de départ élevé" if prediction == 1
            else "Risque de départ faible"
        ),
        "probabilite_depart": round(proba_depart, 4),
        "probabilite_rester": round(proba_reste, 4)
    }