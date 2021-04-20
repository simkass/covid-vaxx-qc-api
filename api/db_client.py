import json

import numpy as np


def merge_establishments(current_establishments, new_establishments):
    establishments = current_establishments

    current_ids = [establishments['id'] for establishments in current_establishments['establishments']]
    new_ids = [establishments['id'] for establishments in new_establishments['establishments']]
    new_ids = np.setdiff1d(new_ids, current_ids)

    for new_id in new_ids:
        establishment_to_add = next(
            (item for item in new_establishments['establishments'] if item['id'] == new_id), None)
        place_to_add = next((item for item in new_establishments['places'] if item['establishment'] == new_id), None)
        dist_to_add = new_establishments['distanceByPlaces'][str(place_to_add['id'])]
        service_to_add = new_establishments['serviceIdsByPlaces'][str(place_to_add['id'])]

        establishments['establishments'].append(establishment_to_add)
        establishments['places'].append(place_to_add)
        establishments['distanceByPlaces'][str(place_to_add['id'])] = dist_to_add
        establishments['serviceIdsByPlaces'][str(place_to_add['id'])] = service_to_add

    return establishments


def post_establishments_of_interest(establishments):
    with open('mock_db/establishments.json', 'r', encoding='utf-8') as f:
        saved_establishments = json.load(f)

    establishments = merge_establishments(saved_establishments, establishments)

    with open('mock_db/establishments.json', 'w+', encoding='utf-8') as f:
        json.dump(establishments, f, ensure_ascii=False, indent=4)


def get_establishments_of_interest():
    with open('mock_db/establishments.json', 'r', encoding='utf-8') as f:
        establishments = json.load(f)
    return establishments


def get_establishment_place_id(establishment_id):
    with open('mock_db/establishments.json', 'r', encoding='utf-8') as f:
        establishments = json.load(f)
    place = next((item for item in establishments['places'] if item['establishment'] == establishment_id), None)
    return place['id']


def get_establishment_place_id(establishment_id, establishments):
    place = next((item for item in establishments['places'] if item['establishment'] == establishment_id), None)
    return place['id']


def get_place_service_id(place_id):
    with open('mock_db/establishments.json', 'r', encoding='utf-8') as f:
        establishments = json.load(f)
    return establishments['serviceIdsByPlaces'][str(place_id)][0]


def get_place_service_id(place_id, establishments):
    return establishments['serviceIdsByPlaces'][str(place_id)][0]


def post_user(user):
    with open('mock_db/users.json', 'w+', encoding='utf-8') as f:
        json.dump(user, f, ensure_ascii=False, indent=4, default=str)
