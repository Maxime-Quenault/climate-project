from flask import Blueprint
from services.meteodataService import getAllMeteodataToJson, getMeteodataByDepartementToJson,getMeteodataByDepartementAndDateToJson, getMeteodataByDepartementAndDatedebutDatefinToJson

meteodata_route = Blueprint('meteodata_route', __name__)

@meteodata_route.route('/getall', methods=['GET'])
def get_meteodata():
    return getAllMeteodataToJson()

@meteodata_route.route('/get/<num_departement>', methods=['GET'])
def get_meteodata_by_departement(num_departement: str):
    return getMeteodataByDepartementToJson(num_departement)

@meteodata_route.route('/get/<num_departement>/<date>', methods=['GET'])
def get_meteodata_by_departement_and_date(num_departement: str, date):
    return getMeteodataByDepartementAndDateToJson(num_departement, date)

@meteodata_route.route('/get/<num_departement>/<datedebut>/<datefin>', methods=['GET'])
def get_meteodata_by_departement_and_datedebut_datefin(num_departement: str, datedebut, datefin):
    return getMeteodataByDepartementAndDatedebutDatefinToJson(num_departement, datedebut, datefin)