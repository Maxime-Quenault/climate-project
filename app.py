from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from departementService import getAllDepartements

load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Se connecter à MongoDB
client = MongoClient(os.getenv('HOSTMONGODBURL'), 5500)
db = client[os.getenv('DATA_BASE')]
collection_departements = db[os.getenv('COLLECTION_DEPARTEMENTS')]
collection_meteo = db[os.getenv('COLLECTION_METEO')]

@app.route('/', methods=['GET'])
def test_connection():
    res = jsonify({'message' : 'OK'})
    return res


# @app.route('/meteo', methods=['GET'])
# def get_meteo_data():
#     station_id = request.args.get('station_id', default=None, type=str)
#     if station_id:
#         data = collection_meteo.find_one({'station_id': station_id})
#     else:
#         data = list(collection_meteo.find())
    
#     # Convertir les données MongoDB en un format JSONifiable
#     data = jsonify([{'station_id': item['station_id'], 'temperature': item['temperature']} for item in data])
#     return data

@app.route('/departements', methods=['GET'])
def get_departements():
    # Récupère tous les départements
    departements = getAllDepartements()

    # Créer une liste de dictionnaires pour chaque département
    departements_list = []
    for dep in departements:
        dep_dict = {
            '_id': str(dep['_id']),  # Convertit ObjectId en string pour JSON
            'num_departement': dep['num_departement'],
            'nom_departement': dep['nom_departement'],
            'stations': dep['stations'],
            'avg_latitude': dep['avg_latitude'],
            'avg_longitude': dep['avg_longitude']
        }
        departements_list.append(dep_dict)

    return jsonify(departements_list)

if __name__ == '__main__':
    app.run(debug=True)

    