from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from api import clic_sante_api

app = Flask(__name__)
CORS(app)


@app.route('/')
@cross_origin(headers=["Content-Type", "Authorization"])
def hello_world():
    return jsonify({'message': 'Api Works!'})


@app.route('/establishments/')
@cross_origin(headers=["Content-Type", "Authorization"])
def get_establishments():
    postal_code = request.args.get('postal_code')
    return clic_sante_api.get_establishments(postal_code)
