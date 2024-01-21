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
    df_scaled = np.reshape(df_scaled, (1, sequence_length, 3))
    

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
    print(predicted_temperature)
    print(f'temperature predis pour le {date_fin_str} matin : {predicted_temperature[0][1]}°C\ntemperature predis pour le {date_fin_str} après-midi : {predicted_temperature[0][2]}°C')

    return predicted_temperature[0]

getPrediction("0000a10bcd38420b81efc24604dc7e99", "72", "2024-01-21", "2024-01-14")

