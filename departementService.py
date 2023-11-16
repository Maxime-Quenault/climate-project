#from model.departementModel import Departement
# from model.stationModel import Station
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

def connectionDataBase():
    client = MongoClient(os.getenv('HOSTMONGODBURL'), 5500)
    db = client[os.getenv('DATA_BASE')]
    collection_departements = db[os.getenv('COLLECTION_DEPARTEMENTS')]
    return collection_departements

def getAllDepartements():
    departements = connectionDataBase().find()
    return departements
