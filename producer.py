from confluent_kafka import Producer
import requests
import json
import os
from dotenv import load_dotenv
import sys
from model.stationModel import Station

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

# Recupération de la liste des station pour un departement


# Effectuer une requête à l'API météo
#Construction de l'url
def build_url(listeStation: Station, token, dateDebut, dateFin):
    url = "https://www.infoclimat.fr/opendata/?method=get&format=json&"
    for station in listeStation:
        url = url + "stations[]=" + station.code + "&"
    url = url + "start=" + dateDebut + "&" + "end=" + dateFin +"&"
    url = url + "token=" + token
    
    return url
#TO DO : Recuperer les infos necessaire (nottament la liste des stations present dans chaque departement) => qu'il faut boucler sur les departements
'''
pour tout les departement faire
    pour chaque semaine de l'annee faire
        recuperer les data via la requete de l'api infoClimat
    fin
fin
envoyer les resutltat dans le kafka 
'''
#api_url = build_url(listeStation?, token_acces, dateDebut?, dateFin?)
# response = requests.get("test")
with open('list_departement.json') as mon_fichier:
    data = json.load(mon_fichier)



# Envoyer les Données dans Kafka
if response.status_code == 200:
    #weather_data = response.json()

    #Convertir les données en chaîne JSON
    #TO DO : Convertir dans les bon objets
    print("test")
    for departement in data: 
        #weather_data_str = json.dumps(weather_data)
        departement_data_str = json.dumps(departement)

        producer.produce("weather_topic", key="data", value=departement_data_str)
        producer.flush()

        print(f"Données envoyées à Kafka avec succès : {departement['nom_departement']}")
else:
    print("La requête à l'API météo a échoué. Code de statut :", response.status_code)
