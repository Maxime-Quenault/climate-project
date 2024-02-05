from flask import Blueprint
from flask import request, jsonify
from services.activiteService import getAllActivityToJson, getActivitiesByPrediction

activite_route = Blueprint('activite_route', __name__)

@activite_route.route('/getall', methods=['GET'])
def get_activities():
    return getAllActivityToJson()

@activite_route.route('/getbyprediction', methods=['POST'])
def get_activities_by_prediction():
    if not request.json:
        return jsonify({'error': 'Missing JSON in request'}), 400
    prediction = request.json
    try:
        activities = getActivitiesByPrediction(prediction)
        return jsonify(activities)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
