from flask import Blueprint
from services.departementService import getAllDepartementsToJson

departement_route = Blueprint('departement_routes', __name__)

@departement_route.route('/getall', methods=['GET'])
def get_departements():
    return getAllDepartementsToJson()