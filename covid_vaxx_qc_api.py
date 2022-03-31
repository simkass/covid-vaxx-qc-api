from faulthandler import disable
import json
from random import randint

import requests
from flask import Flask, request
from flask_cors import CORS, cross_origin

from api import clic_sante_api, config, db_client, email_client, utils

app = Flask(__name__)
CORS(app)

disabled = True
# 31/03/2022
# This service is now disabled as the vaccination campaign in Québec is reaching its end.
# GET Establishments is the only endpoint that still works for demonstration purposes on the web app.
# The other endpoints will return 200 but won't do anything. Again just for demonstration purpose in the web app.
# The notification service has been shut down. Nothing to change in the code.

@app.route('/establishments/', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
def get_establishments():
    lat = request.args.get('lat', None)
    lng = request.args.get('lng', None)
    postal_code = request.args.get('postal_code', "").replace(" ", "")

    if lat == None or lng == None:
        location = clic_sante_api.get_geo_code(postal_code)['results'][0]['geometry']['location']
        return clic_sante_api.get_establishments(postal_code, location['lat'], location['lng'])
    else:
        return clic_sante_api.get_establishments("", lat, lng)

@app.route('/user', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
def post_user():

    if disabled:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    response = request.get_json()

    recaptcha_validation = requests.post("https://www.google.com/recaptcha/api/siteverify",
                                         params={"secret": config.recaptcha_secret, "response": response['recaptcha']})

    recaptcha_validation = json.loads(recaptcha_validation.text)

    if not recaptcha_validation['success']:
        return "Recaptcha validation failed", 400
    else:
        email_address = response['email'].lower()
        if not utils.validate_email_format(email_address):
            return "Email format is invalid", 400

        establishments_of_interest = response['establishments']
        availabilities = response['availabilities']

        db_client.add_user(email_address, establishments_of_interest, availabilities)
        db_client.update_establishments(establishments_of_interest)

        email_client.send_sign_up_email(email_address, establishments_of_interest, availabilities)

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/unsubscribe-request', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
def unsubscription_request():

    if disabled:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    response = request.get_json()
    email_address = response['email'].lower()
    random_code = randint(1000, 9999)
    if db_client.add_pending_unsubscription(email_address, random_code):
        email_client.send_unsubscription_request(email_address, random_code)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    return json.dumps({'success': False,
                       "message": "User doesn't exist in our database. Considered it to be unsubscribed"}), 200, {
        'ContentType': 'application/json'}


@app.route('/unsubscribe', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
def unsubscribe():
        
    if disabled:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    response = request.get_json()
    email_address = response['email'].lower()
    random_code = int(response['random_code'])
    if db_client.unsubscribe(email_address, random_code):
        email_client.send_unsubscription_confirmation(email_address)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    return json.dumps({'success': False,
                       "message": "Confirmation code is invalid for this user"}), 200, {
        'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run()
