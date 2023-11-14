from confluent_kafka import Producer
import requests
import json

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

#api_token = 'ZpGLe4e0nSS0YqEtZvVSAmGF9pwOajmsvhp50btiVMNwe73okBg'
api_url = 'http://www.infoclimat.fr/public-api/gfs/json?_ll=48.85341,2.3488&_auth=CRMDFA5wBCYHKltsVSNVfABoAjcOeAkuA39SMQlsBHlSOV4%2FVDRcOlI8VCkDLAE3U34GZQ41BjZXPApyCXtUNQljA28OZQRjB2hbPlV6VX4AOwJhDjcJNgNoUioJewRkUjZeJFQ2XDlSOVQoAzEBPVN%2BBmMOMgYhVysKbAliVD4JYwNhDm8EYAdsWzhVZ1V%2BACwCZA40CTUDNVI2CTAENlJiXjtUMVw%2BUjhUMQM0AStTZQZmDjgGPVc9CmsJbVQ1CXUDeA4UBBUHdVt5VSdVNAB1An8OZAlvAzQ%3D&_c=de5de0decae02816b4f4ed5455dd257e'

# Effectuer une requête à l'API météo
#headers = {'Authorization': 'Bearer {}'.format(api_token)}
response = requests.get(api_url)

if response.status_code == 200:
    weather_data = response.json()

    # Convertir les données en chaîne JSON
    weather_data_str = json.dumps(weather_data)

    # Envoyer les données à Kafka
    producer.produce("weather_topic", key="data1", value=weather_data_str)

    # Attendre que les messages soient envoyés et confirmés
    producer.flush()

    print("Données envoyées à Kafka avec succès.")
else:
    print("La requête à l'API météo a échoué. Code de statut :", response.status_code)
