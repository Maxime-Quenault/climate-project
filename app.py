from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from routes.departementRoute import departement_route
from routes.meteodataRoute import meteodata_route


load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(departement_route, url_prefix='/departement')
app.register_blueprint(meteodata_route, url_prefix='/meteodata')

@app.route('/ping', methods=['GET'])
def test_connection():
    res = jsonify({'ping' : 'OK'})
    return res

if __name__ == '__main__':
    app.run(debug=True)

    