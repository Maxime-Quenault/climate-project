from dotenv import load_dotenv
from pymongo import MongoClient
import os
import certifi
from models.departementModel import Departement

load_dotenv()

def connectionDataBase():
    client = MongoClient(os.getenv('HOSTMONGODBURL'), tlsCAFile=certifi.where())
    db = client[os.getenv('DATA_BASE')]
    collection_departements = db[os.getenv('COLLECTION_DEPARTEMENTS')]
    return collection_departements

def getAllDepartementsToJson():
    departements = connectionDataBase().find()
    #for dep in departements:
        
    return departements

def getAllDepartementsToObj():
    departements = connectionDataBase().find()
    for dep in departements:
        departement = Departement(**dep)
        print(type(departement))
    return departements
