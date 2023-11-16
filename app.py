from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from routes.departementRoute import departement_route


load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(departement_route, url_prefix='/departement')

# Se connecter à MongoDB
client = MongoClient(os.getenv('HOSTMONGODBURL'), 5500)
db = client[os.getenv('DATA_BASE')]
collection_departements = db[os.getenv('COLLECTION_DEPARTEMENTS')]
collection_meteo = db[os.getenv('COLLECTION_METEO')]

@app.route('/', methods=['GET'])
def test_connection():
    res = jsonify({'message' : 'OK'})
    return res



if __name__ == '__main__':
    app.run(debug=True)

    