import certifi
from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient
import json


# Configuration du consommateur Kafka
def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf

# Création du consommateur
consumer = Consumer(read_ccloud_config("client.properties"))

# S'abonner au topic 'weather_topic'
consumer.subscribe(["weather_topic"])

# Se connecter à MongoDB
try:
    client = MongoClient('mongodb+srv://maximeq72:iw0G1vU7vlgRaBnM@cashflow.rlqlhky.mongodb.net/cashflowDB', tlsCAFile=certifi.where())
    db = client['ClimateDatas']
    collection = db['data']
except Exception as e:
    print(f"Erreur lors de la connexion à MongoDB : {e}")

# Boucle de consommation des messages
cpt = 0
while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    # Récupérer les données du message Kafka
    weather_data_str = msg.value()
    weather_data = json.loads(weather_data_str)

    #print(weather_data_str.decode('utf-8'))

    # Insérer les données dans la collection MongoDB (probleme de TIMEOUT avec mongo dmd à max)
    collection.insert_one(weather_data)

    cpt = cpt + 1
    print(f"Données insérées dans MongoDB avec succès : {cpt}")
