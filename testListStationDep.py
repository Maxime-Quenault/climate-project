from services.departementService import getAllDepartementsToJson
from datetime import datetime, timedelta
from models.stationModel import Station
import os
from dotenv import load_dotenv
import requests

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

date_start = datetime(2008, 1, 1).date()
date_end = datetime(2009, 1, 1).date()

def build_url(liste_stations, token, date_debut, date_fin):
    url = "https://www.infoclimat.fr/opendata/?method=get&format=json&"
    for station in liste_stations:
        url = url + "stations[]=" + station['code_station'] + "&"
    url = url + "start=" + date_debut + "&" + "end=" + date_fin + "&"
    url = url + "token=" + token
    
    return url
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
        if stations:
            print(f"{build_url(stations, token_acces, date_start_up, date_end_up)}\n")
        else:
            print("Aucune station trouvée pour le département :", dep)

        current_date += timedelta(weeks=1)



