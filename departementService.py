from dotenv import load_dotenv
from pymongo import MongoClient
import os
import certifi

load_dotenv()

def connectionDataBase():
    client = MongoClient(os.getenv('HOSTMONGODBURL'), tlsCAFile=certifi.where())
    db = client[os.getenv('DATA_BASE')]
    collection_departements = db[os.getenv('COLLECTION_DEPARTEMENTS')]
    return collection_departements

def getAllDepartements():
    departements = connectionDataBase().find()
    return departements
