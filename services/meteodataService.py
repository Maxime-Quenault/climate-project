import sys
sys.path.append('D:/User/Documents/GitHub/climate-project')
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import certifi
from flask import jsonify
from models.meteoModel import Meteo
import pandas as pd
from services.departementService import connectionDataBaseDep, getAllDepartementsToObj
from tqdm import tqdm

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
        try:
            meteodata_dict = {
                '_id': str(meteo['_id']),
                'departement': meteo['departement'],
                'date': meteo['date'],
                'matin': meteo['matin'],
                'apremidi': meteo['apremidi']
            }
        except KeyError:
            print("l'ID "+str(meteo['_id'])+" pose probleme")
        meteodata_list.append(meteodata_dict)

    return jsonify(meteodata_list)

def getAllMeteodataToObj():

    meteodatas = connectionDataBase().find()
    meteodata_obj = []

    for meteo in meteodatas:

        meteodata = Meteo(**meteo)
        meteodata_obj.append(meteodata)

    return meteodata_obj

def getMeteodataByDepartementToJson(num_departement: str):

    meteodata =  connectionDataBase().find({'departement': num_departement})
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
    
def getMeteodataByDepartementToObj(num_departement: str):

    meteodatas = connectionDataBase().find({'departement': num_departement})
    meteodata_obj = []

    for meteo in meteodatas:

        meteodata = Meteo(**meteo)
        meteodata_obj.append(meteodata)

    return meteodata_obj

def getMeteodataByDepartementAndDateToJson(num_departement: str, date):
    meteo =  connectionDataBase().find_one({'departement': num_departement, 'date': date})

    if meteo:
        meteodata_dict = {
            '_id': str(meteo['_id']),
            'departement': meteo['departement'],
            'date': meteo['date'],
            'matin': meteo['matin'],
            'apremidi': meteo['apremidi']
        }
        return jsonify(meteodata_dict)
    else:
       return jsonify({'message': 'Meteodata not found'}), 404
    
def getMeteodataByDepartementAndDateToObj(num_departement: str, date):

    meteo = connectionDataBase().find_one({'departement': num_departement, 'date': date})

    if meteo:

        meteodata = Meteo(**meteo)
        return meteodata
    
    else:
        return None
    
def getMeteodataByDepartementAndDatedebutDatefinToJson(num_departement: str, datedebut, datefin):
    collection_meteo = connectionDataBase()
    query = {
        'departement': num_departement, 
        'date': {
            '$gte': datedebut,
            '$lte': datefin
        }
    }
    meteo_data_cursor = collection_meteo.find(query)

    meteodata_list = []
    for meteo in meteo_data_cursor:
        meteodata_dict = {
            '_id': str(meteo['_id']),
            'departement': meteo['departement'],
            'date': meteo['date'],
            'matin': meteo['matin'],
            'apremidi': meteo['apremidi']
        }
        meteodata_list.append(meteodata_dict)

    return jsonify(meteodata_list)

def getMeteodataByDepartementAndDatedebutDatefinToObj(num_departement: str, datedebut, datefin):
    collection_meteo = connectionDataBase()
    query = {
        'departement': num_departement, 
        'date': {
            '$gte': datedebut,
            '$lte': datefin
        }
    }
    meteo_data_cursor = collection_meteo.find(query)

    meteo_data_list = []
    for meteo in meteo_data_cursor:

        meteodata = Meteo(**meteo)
        meteo_data_list.append(meteodata)

    return meteo_data_list

def cleanDataBase():
    nb_doublons = 0
    departements = getAllDepartementsToObj()
    connectionDataBaseMeteo = connectionDataBase()
    unique_data = set()

    # dep de 01 à 78 fini !
    for dep in tqdm(departements):
        num_dep = dep.num_departement
        datas = getMeteodataByDepartementToObj(num_dep)

        for data in datas:
            data_key = (data.date, data.departement)
            if data_key in unique_data:
                connectionDataBaseMeteo.delete_one({'date': data.date, 'departement': data.departement})
                nb_doublons += 1
            else:
                unique_data.add(data_key)

    return nb_doublons

# print(f'{cleanDataBase()} données supprimées')