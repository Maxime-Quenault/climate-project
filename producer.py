from confluent_kafka import Producer
import requests
import json
import os
from dotenv import load_dotenv
import sys
from models.stationModel import Station
from services.departementService import getAllDepartementsToJson
from datetime import datetime, timedelta


load_dotenv()

# Utilisez le service ipinfo.io pour obtenir les informations sur votre adresse IP, Ce qui permet de
# choisir le bon token d'acces
response = requests.get("https://ipinfo.io")
data = response.json()
adresse_ip = data['ip']

switch = {
    os.getenv('IP_MAXIME'):os.getenv('TOKEN_MAXIME'),
    os.getenv('IP_JULIEN'):os.getenv('TOKEN_JULIEN'),
    os.getenv('IP_CHARLES'):os.getenv('TOKEN_CHARLES'),
    os.getenv('IP_UNIV'):os.getenv('TOKEN_UNIV')
}

token_acces = switch.get(adresse_ip, None)

if token_acces is None:
    print("Erreur : Aucun Token trouvé pour l'IP de votre machine.")
    sys.exit(1)





# Configuration du producteur Kafka
def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf

# Création du producteur
producer = Producer(read_ccloud_config("client.properties"))

# Effectuer une requête à l'API météo

#Construction de l'url
def build_url(liste_stations, token, date_debut, date_fin):
    url = "https://www.infoclimat.fr/opendata/?method=get&format=json&"
    for station in liste_stations:
        url = url + "stations[]=" + station['code_station'] + "&"
    url = url + "start=" + date_debut + "&" + "end=" + date_fin + "&"
    url = url + "token=" + token

    return url

########---------- TRAITEMENT SPARK ----------
'''
pour tout les departement faire
    pour chaque semaine de l'annee faire
        recuperer les data via la requete de l'api infoClimat
    fin
fin
envoyer les resultats dans le kafka
'''
date_start = datetime(2008, 1, 1).date()
date_end = datetime(2009, 1, 1).date()

# Recupération de la liste des station pour un departement
departements = getAllDepartementsToJson()

# Créer le lien de requete d'API pour chaque département pour chaque semaine
for dep in departements:
    stations = dep['stations']
    current_date = date_start
    while current_date < date_end:
        current_dateWeekLater = current_date + timedelta(weeks=1)
        date_start_up = current_date.strftime("%Y-%m-%d")
        date_end_up = current_dateWeekLater.strftime("%Y-%m-%d")

        api_url = build_url(stations, token_acces, date_start_up, date_end_up)
        response = requests.get(api_url)

        # Envoyer les Données dans Kafka
        if response.status_code == 200:
            weather_data = response.json()

            #Convertir les données en chaîne JSON
            weather_data_str = "EN COURS"

            # Envoyer les données à Kafka
            producer.produce("weather_topic", key="data", value=weather_data_str)

            # Attendre que les messages soient envoyés et confirmés
            producer.flush()
            print("Données envoyées à Kafka avec succès pour le "+date_start_up+" au "+date_end_up)
        else:
            print("La requête à l'API météo a échoué. Code de statut :", response.status_code)

        current_date += timedelta(weeks=1)
