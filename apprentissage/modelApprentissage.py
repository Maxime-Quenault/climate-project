import sys
sys.path.append('D:/User/Documents/GitHub/climate-project')

import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from services.meteodataService import getMeteodataByDepartementToObj


def load_data(num_departement : str):

    data = getMeteodataByDepartementToObj(num_departement)
    data_dicts = [d.to_dict() for d in data]
    df = pd.json_normalize(data_dicts)

    return df

def preprocess_data(df):
    # Convertion de la colonne 'date' en datetime pour l'utiliser comme index
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Sélection des colonnes pertinentes
    df = df[['matin.temperature', 'apremidi.temperature']]

    # On gère les valeurs manquantes et null
    df.dropna(inplace=True)
    indexNamesTempMatin = df[df["matin.temperature"] == 0.0].index
    df.drop(indexNamesTempMatin, inplace=True)
    indexNamesTempApresMidi = df[df["apremidi.temperature"] == 0.0].index
    df.drop(indexNamesTempApresMidi, inplace=True)
    

    # Normalisation des données
    scaler = MinMaxScaler()
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

def train(X_train, y_train, X_test, y_test, sequence_length):
    # Définir le modèle
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(sequence_length, 2)))
    model.add(Dense(1))  # Une seule sortie

    # Compiler le modèle
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Entraîner le modèle
    history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test), verbose=1)

    return model, history

def trace_history(history):
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Losses')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

#Values
sequence_length = 5
num_departement = "72"

#Récupération des données et réalisation de traitements
df = load_data(num_departement)
df_scaled = preprocess_data(df)
X, y = create_sequences_to_LSTM(df_scaled, sequence_length)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Entrainement
model, history = train(X_train, y_train, X_test, y_test, sequence_length)

#Evaluation
test_loss = model.evaluate(X_test, y_test)
print(f"Test Loss: {test_loss}")
trace_history(history)