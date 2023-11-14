from flask import Flask, jsonify, request
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Se connecter à MongoDB
client = MongoClient(os.getenv('HOSTMONGODBURL'), 5500)
db = client[os.getenv('DATA_BASE')]
collection_departements = db[os.getenv('COLLECTION_DEPARTEMENTS')]
collection_meteo = db[os.getenv('COLLECTION_METEO')]

@app.route('/', methods=['GET'])
def test_connection():
    res = jsonify({'message' : 'OK'})
    return res


@app.route('/meteo', methods=['GET'])
def get_meteo_data():
    station_id = request.args.get('station_id', default=None, type=str)
    if station_id:
        data = collection_meteo.find_one({'station_id': station_id})
    else:
        data = list(collection_meteo.find())
    
    # Convertir les données MongoDB en un format JSONifiable
    data = jsonify([{'station_id': item['station_id'], 'temperature': item['temperature']} for item in data])
    return data

@app.route('/departements', methods=['GET'])
def get_departements():
    # Retourne tous les départements
    departements = list(collection_departements.find())
    return jsonify([{'dep_id': dep['dep_id'], 'name': dep['name']} for dep in departements])

if __name__ == '__main__':
    app.run(debug=True)

    