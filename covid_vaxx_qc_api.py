from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from requests.api import get

from api import clic_sante_api, db_client, email_client

app = Flask(__name__)
CORS(app)


@app.route('/')
@cross_origin(headers=["Content-Type", "Authorization"])
def hello_world():
    return jsonify({'message': 'Api Works!'})


@app.route('/establishments/', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
def get_establishments():
    postal_code = request.args.get('postal_code').replace(" ", "")
    location = clic_sante_api.get_geo_code(postal_code)['results'][0]['geometry']['location']
    return clic_sante_api.get_establishments(postal_code, location['lat'], location['lng'])


@app.route('/user', methods=['POST'])
@cross_origin(headers=["Content-Type"])
def post_user():
    response = request.get_json()

    email_address = response['email']
    postal_code = response['postalCode'].replace(" ", "")
    establishments_of_interest = response['establishments']
    availabilities = response['availabilities']

    db_client.add_user(email_address, establishments_of_interest, availabilities)

    location = clic_sante_api.get_geo_code(postal_code)['results'][0]['geometry']['location']
    new_establishments = clic_sante_api.get_establishments(postal_code, location['lat'], location['lng'])
    db_client.update_establishments(establishments_of_interest, new_establishments)

    email_client.send_sign_up_email(email_address, establishments_of_interest, new_establishments, availabilities)
    return ''
