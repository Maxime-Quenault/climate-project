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
client = MongoClient('localhost', 27017)
db = client['eiah']
collection = db['meteo']

# Boucle de consommation des messages
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

    # Insérer les données dans la collection MongoDB
    collection.insert_one(weather_data)

    print("Données insérées dans MongoDB avec succès.")
