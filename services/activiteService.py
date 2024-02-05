import sys
sys.path.append('D:/User/Documents/GitHub/climate-project')
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import certifi
from flask import jsonify
from models.activiteModel import Activite

load_dotenv()

def connectionDataBaseDep():
    client = MongoClient(os.getenv('HOSTMONGODBURL'), tlsCAFile=certifi.where())
    db = client[os.getenv('DATA_BASE')]
    collection_activite = db[os.getenv('COLLECTION_ACTIVITE')]
    return collection_activite

def getAllActivityToJson():
    activities = connectionDataBaseDep().find()
    activities_list = []
    for act in activities:
        act_dict = {
            '_id': str(act['_id']),  # Convertit ObjectId en string pour JSON
            'name': act['name'],
            'departement': act['departement'],
            'latitude': act['latitude'],
            'longitude': act['longitude'],
        }
        activities_list.append(act_dict)

    return jsonify(activities_list)

def getAllActivityToObj():

    activities = connectionDataBaseDep().find()
    activities_obj = []

    for act in activities:

        activite = Activite(**act)
        activities_obj.append(activite)

    return activities_obj

def getActivitiesByPrediction(prediction):

    all_activities = getAllActivityToObj()
    act_dicts = [a.to_dict() for a in all_activities]
    matin_data_outdoor = []
    matin_data_indoor = []
    aprem_data_outdoor = []
    aprem_data_indoor = []

    res = {
        'matin': [],
        'aprem': []
    }

    for act in act_dicts:
        # Outdoor
        if prediction['matin.temperature'] > act['conditions']['temperature_min'] and prediction['matin.pluie_1h'] <= act['conditions']['rainfall_max'] and prediction['matin.vent_moyen'] <= act['conditions']['wind_speed_max']:
            matin_data_outdoor.append(act)
        # Indoor
        else:
            matin_data_indoor.append(act)
        # Outdoor
        if prediction['apremidi.temperature'] > act['conditions']['temperature_min'] and prediction['apremidi.pluie_1h'] <= act['conditions']['rainfall_max'] and prediction['apremidi.vent_moyen'] <= act['conditions']['wind_speed_max']:
            aprem_data_outdoor.append(act)
        # Indoor
        else:
            aprem_data_indoor.append(act)

    res['matin'] = matin_data_outdoor if matin_data_outdoor else matin_data_indoor
    res['aprem'] = aprem_data_outdoor if aprem_data_outdoor else aprem_data_indoor
    
    
    return res