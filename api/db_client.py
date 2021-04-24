import pymongo
from api import config

client = pymongo.MongoClient(config.mongo_connection_string)
db = client['covid-vaxx-qc']
users_collection = db['users']


def add_user(email_address, establishments_of_interest, availabilities):
    users_collection.insert_one({"email_address": email_address,
                                   "establishments_of_interest": establishments_of_interest,
                                   "availabilities": availabilities})