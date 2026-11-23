import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

TEST_EMPLOYE = {
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

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_success():
    response = client.post("/predict", json=TEST_EMPLOYE)
    assert response.status_code == 200
    data = response.json()

    assert data["prediction"] in [0, 1]
    assert data["resultat"] in [
        "Risque de départ élevé",
        "Risque de départ faible"
    ]
    assert 0 <= data["probabilite_depart"] <= 1
    assert 0 <= data["probabilite_rester"] <= 1
    assert (data["probabilite_depart"] + data["probabilite_rester"]) == pytest.approx(1.0, abs=0.0001)

def test_predict_erreur_cat():
    employee = TEST_EMPLOYE.copy()
    employee["genre"] = "Inconnu"

    response = client.post("/predict", json=employee)
    assert response.status_code == 422

def test_predict_erreur_champ():
    employee = TEST_EMPLOYE.copy()
    del employee["age"]

    response = client.post("/predict", json=employee)
    assert response.status_code == 422

def test_predict_erreur_num():
    employee = TEST_EMPLOYE.copy()
    employee["age"] = "trente-cinq"

    response = client.post("/predict", json=employee)
    assert response.status_code == 422

def test_predict_division_0():
    employee = TEST_EMPLOYE.copy()
    employee["annee_experience_totale"] = 0
    employee["annees_dans_l_entreprise"] = 0
    employee["annees_depuis_la_derniere_promotion"] = 0

    response = client.post("/predict", json=employee)
    assert response.status_code == 200