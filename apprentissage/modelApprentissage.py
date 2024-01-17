import sys
sys.path.append('D:/User/Documents/GitHub/climate-project')
from services.meteodataService import getMeteodataByDepartementToObj, getMeteodataByDepartementAndDatedebutDatefinToObj

import pandas as pd
import numpy as np
import math
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt

import mlflow
from mlflow.models.signature import infer_signature
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import Callback
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

scaler = MinMaxScaler()
mlflow.set_experiment("Temperature_Prediction")

class RMSECallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        y_pred = self.model.predict(X_train)
        rmse = math.sqrt(mean_squared_error(y_train, y_pred))
        mlflow.log_metric("rmse", rmse, step=epoch)


def load_data(num_departement : str):

    data = getMeteodataByDepartementToObj(num_departement)
    data_dicts = [d.to_dict() for d in data]
    df = pd.json_normalize(data_dicts)

    return df

def preprocess_data(df):
    # Convertion de la colonne 'date' en datetime pour l'utiliser comme index
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')

    # Sélection des colonnes pertinentes
    df = df[['matin.temperature', 'apremidi.temperature']]

    # On gère les valeurs manquantes et null
    df = df.dropna()
    indexNamesTempMatin = df[df["matin.temperature"] == 999].index
    df = df.drop(indexNamesTempMatin)
    indexNamesTempApresMidi = df[df["apremidi.temperature"] == 999].index
    df = df.drop(indexNamesTempApresMidi)
    

    # Normalisation des données
    df_scaled = scaler.fit_transform(df)

    return df_scaled

def create_sequences_to_LSTM(data, sequence_length):

    sequences = []
    targets = []

    for i in range(len(data) - sequence_length):

        seq = data[i:i + sequence_length]  # Séquence de données
        target = data[i + sequence_length]  # Valeur cible
        sequences.append(seq)
        targets.append(target)

    return np.array(sequences), np.array(targets)

def train(X_train, y_train, X_test, y_test, sequence_length, epochs=3, batch_size=32):
    with mlflow.start_run() as run:
        # Enregistrer les paramètres de formation
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("sequence_length", sequence_length)

        # Définition et compilation du modèle
        model = Sequential()
        model.add(LSTM(50, activation='relu', input_shape=(sequence_length, 2)))
        model.add(Dense(2))
        model.compile(optimizer='adam', loss='mean_squared_error')

        # Entraîner le modèle
        rmse_callback = RMSECallback()
        history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), verbose=1, callbacks=[rmse_callback])


        # Enregistrer les métriques
        for epoch in range(epochs):
            mlflow.log_metric("training_loss", history.history['loss'][epoch], step=epoch)
            mlflow.log_metric("validation_loss", history.history['val_loss'][epoch], step=epoch)

        # Prédiction sur les ensembles d'entraînement et de test
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        signature = infer_signature(X_train, y_pred_train)

        # Calcul des métriques
        train_rmse = math.sqrt(mean_squared_error(y_train, y_pred_train))
        test_rmse = math.sqrt(mean_squared_error(y_test, y_pred_test))
        train_mae = mean_absolute_error(y_train, y_pred_train)
        test_mae = mean_absolute_error(y_test, y_pred_test)
        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)

        # Enregistrement des métriques
        mlflow.log_metrics({"train_rmse": train_rmse, "test_rmse": test_rmse, "train_mae": train_mae, "test_mae": test_mae, "train_r2": train_r2, "test_r2": test_r2})


        # Enregistrer le modèle
        mlflow.tensorflow.log_model(model, "model", signature=signature)

    return model, history

def get_prediction(model, sequence_length, num_departement):
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


#Values
sequence_length = 365
num_departement = "72"
epochs = 10
batch_size = 64

#Récupération des données et réalisation de traitements
df = load_data(num_departement)
df_scaled = preprocess_data(df)
X, y = create_sequences_to_LSTM(df_scaled, sequence_length)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Entrainement
model, history = train(X_train, y_train, X_test, y_test, sequence_length, epochs=epochs, batch_size=batch_size)

#Evaluation
test_loss = model.evaluate(X_test, y_test)

#Utilisation
prediction = get_prediction(model, sequence_length, num_departement)




