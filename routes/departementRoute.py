from flask import Blueprint
from services.departementService import getAllDepartementsToJson, getDepartementByNumToJson

departement_route = Blueprint('departement_routes', __name__)

@departement_route.route('/getall', methods=['GET'])
def get_departements():
    return getAllDepartementsToJson()

@departement_route.route('/get/<num_departement>', methods=['GET'])
def get_departement_by_num(num_departement: str):
    return getDepartementByNumToJson(num_departement)