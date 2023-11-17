from dotenv import load_dotenv
from pymongo import MongoClient
import os
import certifi
from flask import jsonify
from models.meteoModel import Meteo

load_dotenv()

def connectionDataBase():
    client = MongoClient(os.getenv('HOSTMONGODBURL'), tlsCAFile=certifi.where())
    db = client[os.getenv('DATA_BASE')]
    collection_departements = db[os.getenv('COLLECTION_METEO')]
    return collection_departements

def getAllMeteodataToJson():
    meteodata = connectionDataBase().find()
    meteodata_list = []
    for meteo in meteodata:
        meteodata_dict = {
            '_id': str(meteo['_id']),
            'departement': meteo['departement'],
            'date': meteo['date'],
            'matin': meteo['matin'],
            'apremidi': meteo['apremidi']
        }
        meteodata_list.append(meteodata_dict)

    return jsonify(meteodata_list)

def getAllMeteodataToObj():

    meteodatas = connectionDataBase().find()
    meteodata_obj = []

    for meteo in meteodatas:

        meteodata = Meteo(**meteo)
        meteodata_obj.insert(meteodata)

    return meteodata_obj