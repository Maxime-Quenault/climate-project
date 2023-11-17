from flask import Blueprint
from services.meteodataService import getAllMeteodataToJson

meteodata_route = Blueprint('meteodata_route', __name__)

@meteodata_route.route('/getall', methods=['GET'])
def get_meteodata():
    return getAllMeteodataToJson()