import pymongo
from bson.json_util import dumps

from api import clic_sante_api, config

client = pymongo.MongoClient(config.mongo_connection_string)
db = client['covid-vaxx-qc']

users_collection = db['users']
establishments_collection = db['establishments']
availabilities_collection = db['availabilities']


def add_user(email_address, establishments_of_interest, availabilities):
    existing_user = users_collection.find({'email_address': email_address})

    if users_collection.count_documents({'email_address': email_address}) == 0:
        users_collection.insert_one({"email_address": email_address,
                                     "establishments_of_interest": establishments_of_interest,
                                     "availabilities": availabilities, 'new_user': True})
    else:
        establishments_of_interest = list(
            set(existing_user[0]['establishments_of_interest'] + establishments_of_interest))
        availabilities = existing_user[0]['availabilities'] + availabilities
        users_collection.update(
            {'email_address': email_address},
            {'email_address': email_address, 'establishments_of_interest': establishments_of_interest,
             'availabilities': availabilities, 'new_user': True})


def update_establishments(establishments_of_interest, new_establishments):
    new_places = new_establishments['places']

    for establishment_id in establishments_of_interest:
        if establishments_collection.count_documents({"id": establishment_id}) == 0:
            establishment = next((place for place in new_places if place['id'] == establishment_id), None)
            if establishment is not None:
                establishment['service'] = clic_sante_api.get_establishment_service(establishment['establishment'])
                establishments_collection.insert_one(establishment)


def get_users():
    return dumps(list(users_collection.find({})), indent=2)


def get_establishments():
    return dumps(list(establishments_collection.find({})), indent=2)


def get_availabilities():
    return dumps(list(availabilities_collection.find({})), indent=2)
