from dotenv import load_dotenv
from pymongo import MongoClient
import os
import certifi
from flask import jsonify
from models.departementModel import Departement

load_dotenv()

def connectionDataBase():
    client = MongoClient(os.getenv('HOSTMONGODBURL'), tlsCAFile=certifi.where())
    db = client[os.getenv('DATA_BASE')]
    collection_departements = db[os.getenv('COLLECTION_DEPARTEMENTS')]
    return collection_departements

def getAllDepartementsToJson():
    departements = connectionDataBase().find()
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

def getAllDepartementsToObj():

    departements = connectionDataBase().find()
    departement_obj = []

    for dep in departements:

        departement = Departement(**dep)
        departement_obj.insert(departement)

    return departement_obj
