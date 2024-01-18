from flask import Blueprint
from apprentissage.prediction import getPrediction

meteodata_route = Blueprint('prediction_route', __name__)

@meteodata_route.route('/get/<num_departement>', methods=['GET'])
def get_prediction(num_departement: str, date: str):
    #TO DO : changer le format de retour, transformer le vecteur en json pour le front
    return getPrediction("2642afa4fc584d26838f47051ab7f1ed", num_departement, date)