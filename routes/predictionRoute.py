from flask import Blueprint, jsonify
from apprentissage.prediction import getPrediction

prediction_route = Blueprint('prediction_route', __name__)

@prediction_route.route('/get/<num_departement>/<date>', methods=['GET'])
def get_prediction(num_departement: str, date: str):
    #TO DO : changer le format de retour, transformer le vecteur en json pour le front
    return jsonify(getPrediction("c5bcb6c4c9f04954856f6de70973751d", num_departement, date, "2024-01-14"))