import pytest
from app.preprocessing import prepare_employee_data

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

def test_ratio_anciennete_experience():
    result = prepare_employee_data(TEST_EMPLOYE)
    assert result["ratio_anciennete_experience"].iloc[0] == 0.5

def test_ratio_evolution_poste():
    result = prepare_employee_data(TEST_EMPLOYE)
    assert result["ratio_evolution_poste"].iloc[0] == 0.2

def test_score_satisfaction_global():
    result = prepare_employee_data(TEST_EMPLOYE)
    assert result["score_satisfaction_global"].iloc[0] == 3.0

def test_ratio_anciennete_division_zero():
    employee = TEST_EMPLOYE.copy()
    employee["annee_experience_totale"] = 0

    result = prepare_employee_data(employee)
    assert result["ratio_anciennete_experience"].iloc[0] == 0

def test_ratio_evolution_division_zero():
    employee = TEST_EMPLOYE.copy()
    employee["annees_dans_l_entreprise"] = 0

    result = prepare_employee_data(employee)
    assert result["ratio_evolution_poste"].iloc[0] == 0

def test_score_satisfaction_moyenne():
    employee = TEST_EMPLOYE.copy()
    employee["satisfaction_employee_environnement"] = 1
    employee["satisfaction_employee_nature_travail"] = 2
    employee["satisfaction_employee_equipe"] = 3
    employee["satisfaction_employee_equilibre_pro_perso"] = 4

    result = prepare_employee_data(employee)
    assert result["score_satisfaction_global"].iloc[0] == 2.5