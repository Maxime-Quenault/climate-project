from confluent_kafka import Producer
import requests
import json
import time
import os
from dotenv import load_dotenv
import sys
from models.stationModel import Station
from services.departementService import connectionDataBase, getAllDepartementsToJson
from datetime import datetime, timedelta
import pyspark
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import col, struct, sum, avg, mean, round, date_format, when, lower, lit, udf, expr, explode, lit, explode_outer, hour
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType


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
date_start = datetime(2022, 1, 1).date()
date_end = datetime(2023, 1, 1).date()

# Recupération de la liste des station pour un departement
departements = connectionDataBase().find()

# Créer le lien de requete d'API pour chaque département pour chaque semaine
# dep 58 pas fait
for dep in departements[58:]:
    stations = dep['stations']
    code_departement = dep['num_departement']
    current_date = date_start
    while current_date < date_end:
        current_dateWeekLater = current_date + timedelta(weeks=1) - timedelta(days=1)
        date_start_up = current_date.strftime("%Y-%m-%d")
        date_end_up = current_dateWeekLater.strftime("%Y-%m-%d")

        api_url = build_url(stations, token_acces, date_start_up, date_end_up)

        response = requests.get(api_url)

        # Envoyer les Données dans Kafka
        if response.status_code == 200:

            # Convertir les données en chaîne JSON et création du fichier de traitement
            weather_data = response.json()
            path_name = "datas/weather_test.json"

            max_retries = 10
            retry_delay = 1  # en secondes

            #Si il échoue il recommence
            for attempt in range(max_retries):
                try:
                    with open(path_name, 'w') as fichier_json:
                        json.dump(weather_data, fichier_json)
                    break  # Si l'opération réussit, sortez de la boucle
                except PermissionError:
                    print(f"Erreur de permission lors de la tentative {attempt + 1}. Réessai dans {retry_delay} secondes.")
                    time.sleep(retry_delay)
            
            # Création du DataFrame Spark
            spark = SparkSession.builder.appName('bigDataApp').getOrCreate()
            spark.sparkContext.setLogLevel("ERROR") 
            spark.conf.set("spark.sql.repl.eagerEval.enabled", True)

            df_weather = spark.read.option("multiLine", True).json(path_name).cache()
            
            # Get the list of column names that contain the expected array structure
            # Exclude '_params' or any other non-relevant fields
            relevant_columns = [col for col in df_weather.select("hourly.*").columns if col != '_params']

            # Exploding each station's hourly data into separate DataFrames
            dfs = []
            for station in relevant_columns:
                df_station = df_weather.select(explode(col(f"hourly.{station}")).alias("hourly_data"))
                
                # Check if hourly_data is a struct and expand it accordingly
                if isinstance(df_station.schema["hourly_data"].dataType, StructType):
                    df_station = df_station.select("hourly_data.*")
                else:
                    # Skip this station if the data is not in the expected format
                    continue

                dfs.append(df_station)
            
            # On regarde si il y a des données
            if not bool(dfs):
                
                print(f"AUCUNE DONNEE POUR LE DEP :{code_departement} de la période {date_start_up} - {date_end_up}.")
            
            else:
                # Union all the DataFrames into one, ensuring they all have the same schema
                df_combined = dfs[0]
                # Vérifie si la colonne "nebulosite" existe
                if "nebulosite" not in df_combined.columns:
                    # Si elle n'existe pas, la créer avec des valeurs nulles
                    df_combined = df_combined.withColumn("nebulosite", lit(None).cast(DoubleType()))

                # Vérifie si la colonne "neige_au_sol" existe
                if "neige_au_sol" not in df_combined.columns:
                    # Si elle n'existe pas, la créer avec des valeurs nulles
                    df_combined = df_combined.withColumn("neige_au_sol", lit(None).cast(DoubleType()))

                # Vérifie si la colonne "neige_au_sol" existe
                if "temps_omm" not in df_combined.columns:
                    # Si elle n'existe pas, la créer avec des valeurs nulles
                    df_combined = df_combined.withColumn("temps_omm", lit(None).cast(DoubleType()))
                
                # Vérifie si la colonne "visibilite" existe
                if "visibilite" not in df_combined.columns:
                    # Si elle n'existe pas, la créer avec des valeurs nulles
                    df_combined = df_combined.withColumn("visibilite", lit(None).cast(DoubleType()))

                # Vérifie si la colonne "visibilite" existe
                if "pluie_3h" not in df_combined.columns:
                    # Si elle n'existe pas, la créer avec des valeurs nulles
                    df_combined = df_combined.withColumn("pluie_3h", lit(None).cast(DoubleType()))

                    

                for df in dfs[1:]:
                    # Vérifie si la colonne "nebulosite" existe
                    if "nebulosite" not in df.columns:
                        # Si elle n'existe pas, la créer avec des valeurs nulles
                        df = df.withColumn("nebulosite", lit(None).cast(DoubleType()))

                    # Vérifie si la colonne "neige_au_sol" existe
                    if "neige_au_sol" not in df.columns:
                        # Si elle n'existe pas, la créer avec des valeurs nulles
                        df = df.withColumn("neige_au_sol", lit(None).cast(DoubleType()))

                    # Vérifie si la colonne "neige_au_sol" existe
                    if "temps_omm" not in df.columns:
                        # Si elle n'existe pas, la créer avec des valeurs nulles
                        df = df.withColumn("temps_omm", lit(None).cast(DoubleType()))

                    # Vérifie si la colonne "visibilite" existe
                    if "visibilite" not in df.columns:
                        # Si elle n'existe pas, la créer avec des valeurs nulles
                        df = df.withColumn("visibilite", lit(None).cast(DoubleType()))

                    # Vérifie si la colonne "visibilite" existe
                    if "pluie_3h" not in df.columns:
                        # Si elle n'existe pas, la créer avec des valeurs nulles
                        df = df.withColumn("pluie_3h", lit(None).cast(DoubleType()))
                    
                    df_combined = df_combined.unionByName(df)

                df_result = df_combined

                # Ajouter une colonne pour la demi-journée (AM ou PM)
                df_result = df_result.withColumn("Mi-journée", when((hour(col("dh_utc")) >= 6) & (hour(col("dh_utc")) < 12), "AM").when((hour(col("dh_utc")) >= 12) & (hour(col("dh_utc")) < 20), "PM"))

                # Ajouter une colonne pour le jour
                df_result = df_result.withColumn("date", date_format(col("dh_utc"), "yyyy-MM-dd"))


                # Regroupement par jour avec les données structurées par période
                result_json = df_result.groupBy("date").pivot("Mi-journée", ["AM", "PM"]).agg(
                    struct(
                        round(avg("temperature"), 2).alias("temperature"),
                        round(avg("nebulosite"), 2).alias("nebulosite"),
                        round(avg("pression"), 2).alias("pression"),
                        round(avg("humidite"), 2).alias("humidite"),
                        round(avg("point_de_rosee"), 2).alias("point_de_rosee"),
                        round(avg("vent_moyen"), 2).alias("vent_moyen"),
                        round(avg("vent_rafales"), 2).alias("vent_rafales"),
                        round(avg("vent_direction"), 2).alias("vent_direction"),
                        round(avg("pluie_1h"), 2).alias("pluie_1h"),
                        round(avg("pluie_3h"), 2).alias("pluie_3h"),
                        round(avg("neige_au_sol"), 2).alias("neige_au_sol")
                    )
                ).sort("date").withColumn("departement",lit(code_departement))

                # Renommer les colonnes
                result_json = result_json.withColumnRenamed("AM", "matin").withColumnRenamed("PM", "apremidi")

                result_json = result_json.select("departement","date","matin","apremidi")
                
                print(result_json)
                
                # Définir le chemin du fichier de sortie CSV
                output_path = './datas_meteo.json'

                json_array = result_json.toJSON().collect()

                # Envoyer les données à Kafka
                for i, json_entry in enumerate(json_array, 1):
                    producer.produce("weather_topic", key="data", value=json_entry)
                    print(f"Donnée n°{i}/{len(json_array)}, DEP : {code_departement} | Du {date_start_up} - {date_end_up} envoyée à Kafka avec succès.")

                    # Attendre que les messages soient envoyés et confirmés
                    producer.flush()
                
        else:
            print("La requête à l'API météo a échoué. Code de statut :", response.status_code)

        # Ferme la session spark
        spark.stop()
        current_date += timedelta(weeks=1)

    print(f"TOUTES LES DONNEES DU DEP :{code_departement} a été envoyée du {date_start} - {date_end} à kafka.")

print("***** INSERTION DES DONNEES POUR TOUS LES DEPARTEMENTS REUSSIE ! *****")
