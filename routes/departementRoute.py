from flask import Blueprint, jsonify
from departementService import getAllDepartements

departement_route = Blueprint('departement_routes', __name__)

@departement_route.route('/getall', methods=['GET'])
def get_departements():
    # Récupère tous les départements
    departements = getAllDepartements()

    # Créer une liste de dictionnaires pour chaque département
    departements_list = []
    for dep in departements:
        dep_dict = {
            '_id': str(dep['_id']),  # Convertit ObjectId en string pour JSON
            'num_departement': dep['num_departement'],
            'nom_departement': dep['nom_departement'],
            'stations': dep['stations'],
            'avg_latitude': dep['avg_latitude'],
            'avg_longitude': dep['avg_longitude']
        }
        departements_list.append(dep_dict)

    return jsonify(departements_list)