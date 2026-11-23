import pandas as pd

def prepare_employee_data(employee_data: dict) -> pd.DataFrame:
    input_data = pd.DataFrame([employee_data])

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

    return input_data