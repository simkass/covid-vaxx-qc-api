import json
import numpy as np
from datetime import datetime
from api.clic_sante_api import get_establishments, get_establishment_days, get_establishment_schedule

def choose_establishments(option, establishments):
    # Option 0, choose all establishments
    if option==0:
        return [establishment['id'] for establishment in establishments['establishments']]
    return []

def choose_dates():
    return 0 

def merge_establishments(current_establishments, new_establishments):
    establishments = current_establishments

    current_ids = [establishments['id'] for establishments in current_establishments['establishments']]
    new_ids = [establishments['id'] for establishments in new_establishments['establishments']]
    new_ids = np.setdiff1d(new_ids, current_ids)

    for new_id in new_ids:
        establishment_to_add = next((item for item in new_establishments['establishments'] if item['id'] == new_id), None)
        place_to_add = next((item for item in new_establishments['places'] if item['establishment'] == new_id), None)
        dist_to_add = new_establishments['distanceByPlaces'][str(place_to_add['id'])]
        service_to_add = new_establishments['serviceIdsByPlaces'][str(place_to_add['id'])]

        establishments['establishments'].append(establishment_to_add)
        establishments['places'].append(place_to_add)
        establishments['distanceByPlaces'][str(place_to_add['id'])] = dist_to_add
        establishments['serviceIdsByPlaces'][str(place_to_add['id'])] = service_to_add
    
    return establishments

def save_establishments(establishments):
    with open('mock_db/establishments.json', 'r', encoding='utf-8') as f:
        saved_establishments = json.load(f)
    establishments = merge_establishments(saved_establishments, establishments)
    with open('mock_db/establishments.json', 'w+', encoding='utf-8') as f:
        json.dump(establishments, f, ensure_ascii=False, indent=4)

def get_establishment_place_id(establishment_id):
    with open('mock_db/establishments.json', 'r', encoding='utf-8') as f:
         establishments = json.load(f)
    place = next((item for item in establishments['places'] if item['establishment'] == establishment_id), None)
    return place['id']

def get_place_service_id(place_id):
    with open('mock_db/establishments.json', 'r', encoding='utf-8') as f:
        establishments = json.load(f)
    return establishments['serviceIdsByPlaces'][str(place_id)][0]


def main():
    email = 'test@gmail.com'
    postal_code = 'J4B 6X0'

    establishments = get_establishments(postal_code)

    save_establishments(establishments)

    place_id = get_establishment_place_id(70016)
    service_id = get_place_service_id(place_id)

    chosen_places = choose_establishments(0, establishments)

    days = get_establishment_days(70016, place_id, service_id)

    schedule = get_establishment_schedule(70016, place_id, service_id, datetime(2021, 4, 4), datetime(2022, 10, 4))

if __name__=='__main__':
    main()