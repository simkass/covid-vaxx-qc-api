import json
from random import randint

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from requests.api import get

from api import clic_sante_api, db_client, email_client, utils

app = Flask(__name__)
CORS(app)


@app.route('/establishments/', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
def get_establishments():
    postal_code = request.args.get('postal_code').replace(" ", "")
    location = clic_sante_api.get_geo_code(postal_code)['results'][0]['geometry']['location']
    return clic_sante_api.get_establishments(postal_code, location['lat'], location['lng'])


@app.route('/user', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
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
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/unsubscribe-request', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
def unsubscription_request():
    response = request.get_json()
    email_address = response['email']
    random_code = randint(1000, 9999)
    if db_client.add_pending_unsubscription(email_address, random_code):
        email_client.send_unsubscription_request(email_address, random_code)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}


@app.route('/unsubscribe', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
def unsubscribe():
    response = request.get_json()
    email_address = response['email']
    random_code = int(response['random_code'])
    if db_client.unsubscribe(email_address, random_code):
        email_client.send_unsubscription_confirmation(email_address)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run()
