import pymongo
from api import config

client = pymongo.MongoClient(config.mongo_connection_string)
db = client['covid-vaxx-qc']
users_collection = db['users']


def add_user(email_address, establishments_of_interest, availabilities):
    existing_user = users_collection.find({'email_address': email_address})
    if existing_user.count == 0:
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


# e = 'hello@snake.com'
# est = [100, 120, 5873]
# avail = [{"start_datetime":
#           "2021-04-24T00:20",
#           "end_datetime":
#           "2022-04-24T12:20"}]

# add_user(e, est, avail)
