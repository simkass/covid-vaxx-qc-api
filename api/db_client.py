import pymongo

from api import clic_sante_api, config

client = pymongo.MongoClient(config.mongo_connection_string)
db = client['covid-vaxx-qc']
users_collection = db['users']
establishments_collection = db['establishments']


def add_user(email_address, establishments_of_interest, availabilities):
    existing_user = users_collection.find({'email_address': email_address})

    if users_collection.count_documents({'email_address': email_address}) == 0:
        users_collection.insert_one({"email_address": email_address,
                                     "establishments_of_interest": establishments_of_interest,
                                     "availabilities": availabilities})
    else:
        establishments_of_interest = list(
            set(existing_user[0]['establishments_of_interest'] + establishments_of_interest))
        availabilities = existing_user[0]['availabilities'] + availabilities
        users_collection.update(
            {'email_address': email_address},
            {'email_address': email_address, 'establishments_of_interest': establishments_of_interest,
             'availabilities': availabilities})


def update_establishments(postal_code, establishments_of_interest):
    location = clic_sante_api.get_geo_code(postal_code)['results'][0]['geometry']['location']
    new_establishments = clic_sante_api.get_establishments(postal_code, location['lat'], location['lng'])
    new_places = new_establishments['places']

    for establishment_id in establishments_of_interest:
        if establishments_collection.count_documents({"establishment": establishment_id}) == 0:
            establishment = next((place for place in new_places if place['establishment'] == establishment_id), None)

            if establishment is not None:
                establishment['service'] = clic_sante_api.get_establishment_service(establishment_id)
                establishments_collection.insert_one(establishment)


# e = 'hello@snake.com'
# est = [100, 120, 5873]
# avail = [{"start_datetime":
#           "2021-04-24T00:20",
#           "end_datetime":
#           "2022-04-24T12:20"}]

# add_user(e, est, avail)

# update_establishments('j2h1e4', [61612, 60049, 60046])
