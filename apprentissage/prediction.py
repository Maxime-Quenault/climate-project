import sys
sys.path.append('D:/User/Documents/GitHub/climate-project')
from services.meteodataService import getMeteodataByDepartementAndDatedebutDatefinToObj
from apprentissage import preprocess_data, get_param_apprentissage

import pandas as pd
import numpy as np
import math
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt
import mlflow


def getPrediction(id_model, num_departement, date_prediction_str, date_connue_plus_ancienne):

    # Récupérations des paramètres d'apprentissage
    model = mlflow.tensorflow.load_model(f"runs:/{id_model}/model")
    param_apprentissage = get_param_apprentissage()
    sequence_length = param_apprentissage['sequence_length']
    scaler = param_apprentissage['scaler']

    # Mise en place des dates pour la sequences utilisé pour la prédiction
    date_prediction = datetime.strptime(date_prediction_str, "%Y-%m-%d").date()
    date_fin = datetime.strptime(date_connue_plus_ancienne, "%Y-%m-%d").date()
    date_debut = date_fin - timedelta(days=sequence_length-1)
    date_fin_str = date_fin.strftime("%Y-%m-%d")
    date_debut_str = date_debut.strftime("%Y-%m-%d")

    # Récupération des vecteurs d'entrée pour la prédiction
    data = getMeteodataByDepartementAndDatedebutDatefinToObj(num_departement, date_debut_str, date_fin_str)
    data_dicts = [d.to_dict() for d in data]
    df = pd.json_normalize(data_dicts)
    df_scaled = preprocess_data(df)
    df_scaled = np.reshape(df_scaled, (1, sequence_length, 17))
    

    while date_fin < date_prediction:

        # Calcul de la prédiction
        new_prediction = model.predict(df_scaled)
        predicted_temperature = scaler.inverse_transform(new_prediction)

        # Mise à jour de la sequence de prediction
        updated_sequence = np.delete(df_scaled[0], 0, axis=0)
        updated_sequence = np.append(updated_sequence, [predicted_temperature[0]], axis=0)

        # Mettre à jour les dates pour la prochaine prédiction
        date_fin = date_fin + timedelta(days=1)
        date_debut = date_fin - timedelta(days=sequence_length-1)


    date_fin_str = date_fin.strftime("%Y-%m-%d")
    prediction = predicted_temperature[0]
    prediction_res = {
        'departement' : prediction[0], 
             'matin.temperature' : prediction[1], 
             'matin.pression' : prediction[2], 
             'matin.humidite' : prediction[3], 
             'matin.vent_moyen' : prediction[4],
             'matin.vent_rafales' : prediction[5],
             'matin.vent_direction' : prediction[6],
             'matin.pluie_1h' : prediction[7],
             'matin.pluie_3h' : prediction[8],
             'apremidi.temperature' : prediction[9],
             'apremidi.pression' : prediction[10], 
             'apremidi.humidite' : prediction[11], 
             'apremidi.vent_moyen' : prediction[12],
             'apremidi.vent_rafales' : prediction[13],
             'apremidi.vent_direction' : prediction[14],
             'apremidi.pluie_1h' : prediction[15],
             'apremidi.pluie_3h' : prediction[16]
    }
    return prediction_res

print(getPrediction("c8bba4e619b34d39bb2b51c2b1f5ad00", "58", "2024-01-24", "2024-01-14"))
