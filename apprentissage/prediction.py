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


def get_prediction(id_model, num_departement, date_prediction):

    model = mlflow.tensorflow.load_model(f"runs:/{id_model}/model")
    param_apprentissage = get_param_apprentissage()
    sequence_length = param_apprentissage['sequence_length']
    scaler = param_apprentissage['scaler']

    date_fin = datetime(2024, 1, 14).date()
    date_debut = date_fin - timedelta(days=sequence_length-1)

    date_fin_str = date_fin.strftime("%Y-%m-%d")
    date_debut_str = date_debut.strftime("%Y-%m-%d")

    data = getMeteodataByDepartementAndDatedebutDatefinToObj(num_departement, date_debut_str, date_fin_str)
    data_dicts = [d.to_dict() for d in data]
    df = pd.json_normalize(data_dicts)
    df_scaled = preprocess_data(df)
    df_scaled = np.reshape(df_scaled, (1, sequence_length, 2))

    new_prediction = model.predict(df_scaled)
    predicted_temperature = scaler.inverse_transform(new_prediction)
    print(f'temperature predis pour le {date_fin_str} matin : {predicted_temperature[0][0]}°C\ntemperature predis pour le {date_fin_str} après-midi : {predicted_temperature[0][1]}°C')

    return predicted_temperature[0]

get_prediction("2642afa4fc584d26838f47051ab7f1ed", "72", "2024-05-03")

