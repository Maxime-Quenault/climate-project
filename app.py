from flask import Flask, json, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import numpy as np
from routes.departementRoute import departement_route
from routes.meteodataRoute import meteodata_route
from routes.predictionRoute import prediction_route
from routes.activiteRoute import activite_route


load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(departement_route, url_prefix='/departement')
app.register_blueprint(meteodata_route, url_prefix='/meteodata')
app.register_blueprint(prediction_route, url_prefix='/prediction')
app.register_blueprint(activite_route, url_prefix='/activities')

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder

@app.route('/ping', methods=['GET'])
def test_connection():
    res = jsonify({'ping' : 'OK'})
    return res

if __name__ == '__main__':
    app.run(debug=True, port=8000)

    