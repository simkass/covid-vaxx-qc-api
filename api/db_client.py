import pymongo
from bson.json_util import dumps

from api import clic_sante_api, config

client = pymongo.MongoClient(config.mongo_connection_string)
db = client[config.mongo_db]

users_collection = db['users']
establishments_collection = db['establishments']
availabilities_collection = db['availabilities']
pending_unsubscription = db['pending-unsubscriptions']


def add_user(email_address, establishments_of_interest, availabilities):
    existing_user = users_collection.find({'email_address': email_address})
    establishement_ids = [establishment['id']
                          for establishment in establishments_of_interest]
    if users_collection.count_documents({'email_address': email_address}) == 0:
        users_collection.insert_one({"email_address": email_address,
                                     "establishments_of_interest": establishement_ids,
                                     "availabilities": availabilities, 'new_user': True,
                                     'hours_since_last_email': config.notif_delay})
    else:
        establishments_of_interest = list(
            set(existing_user[0]['establishments_of_interest'] + establishement_ids))
        availabilities = existing_user[0]['availabilities'] + availabilities
        users_collection.update(
            {'email_address': email_address},
            {'email_address': email_address, 'establishments_of_interest': establishments_of_interest,
             'availabilities': availabilities, 'new_user': True, 'hours_since_last_email': config.notif_delay})


def toggle_new_user(email_address):
    existing_user = users_collection.find({'email_address': email_address})
    establishments_of_interest = list(
        set(existing_user[0]['establishments_of_interest']))
    availabilities = existing_user[0]['availabilities']
    hours = existing_user[0]['hours_since_last_email']

    users_collection.update(
        {'email_address': email_address},
        {'email_address': email_address, 'establishments_of_interest': establishments_of_interest,
         'availabilities': availabilities, 'new_user': False, 'hours_since_last_email': hours})


def update_user_hours_since_last_email(email_address, hours):
    existing_user = users_collection.find({'email_address': email_address})
    establishments_of_interest = list(
        set(existing_user[0]['establishments_of_interest']))
    availabilities = existing_user[0]['availabilities']
    new_user = existing_user[0]['new_user']

    users_collection.update(
        {'email_address': email_address},
        {'email_address': email_address, 'establishments_of_interest': establishments_of_interest,
         'availabilities': availabilities, 'new_user': new_user, 'hours_since_last_email': hours})


def update_establishments(establishments_of_interest):

    for selected_establishment in establishments_of_interest:
        if establishments_collection.count_documents({"id": selected_establishment['id']}) == 0:
            # establishment = next((place for place in new_places if place['id'] == establishment_id), None)
            establishment = selected_establishment
            if establishment is not None:
                establishment['service'] = clic_sante_api.get_establishment_service(
                    establishment['establishment'])
                establishments_collection.insert_one(establishment)


def get_users():
    return list(users_collection.find({}))


def get_establishments():
    return list(establishments_collection.find({}))


def get_availabilities():
    return list(availabilities_collection.find({}))


def update_availabilities(availabilities):
    availabilities_collection.remove({})
    for availability in availabilities:
        availabilities_collection.insert_one(availability)


def add_pending_unsubscription(email_address, random_code):
    if users_collection.count_documents({"email_address": email_address}) != 0:
        pending_unsubscription.insert_one(
            {'email_address': email_address, 'random_code': random_code})
        return True
    return False


def unsubscribe(email_address, random_code):
    if pending_unsubscription.count_documents({'email_address': email_address, 'random_code': random_code}) != 0:
        pending_unsubscription.remove({'email_address': email_address})
        users_collection.remove({'email_address': email_address})
        return True
    return False
