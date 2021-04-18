import json
from datetime import datetime
import pandas as pd
import numpy as np

from api.clic_sante_api import (get_establishment_days,
                                get_establishment_schedule, get_establishments)
from api.covid_vaxx_qc_api import (get_establishment_place_id,
                                   get_place_service_id, post_establishments_of_interest,
                                   post_user, get_establishments_of_interest)


def choose_establishments(option, establishments):
    # Option 0, choose all establishments
    if option == 0:
        return [establishment['id'] for establishment in establishments['establishments']]
    return []


def choose_dates():
    return 0


def user_sign_up():
    print("Enter your email address")
    email_address = input()
    print("Enter your postal code")
    postal_code = input()

    establishments = get_establishments(postal_code)
    post_establishments_of_interest(establishments)

    print("Available establishments")

    for establishment in establishments['establishments']:
        print('id: ' + str(establishment['id']
                           ) + ' - ' + establishment['name'] + ' - ' + establishment['address'] + '\n')

    establishments_of_interest = []
    picking_establishments = True
    while picking_establishments:
        print("Pick establishments of interest by id or by writing 0 to pick all")
        pick = input()
        if pick == '0':
            picking_establishments = False
            establishments_of_interest = [establishment['id'] for establishment in establishments['establishments']]
        else:
            establishments_of_interest.append(int(pick))
            print("Continue picking establishments? (Y, N)")
            if input() != 'Y':
                picking_establishments = False

    dates_of_interest = []
    choosing_dates = True
    while choosing_dates:
        print("Choose a date for which you would want to be notified in the following format: year-month-day")
        date_str = input()
        start_date = datetime.strptime(date_str, '%Y-%m-%d')
        end_date = start_date
        print("From what time are you available on that day? H:M")
        start_time_str = input()
        start_date = start_date.replace(hour=int(start_time_str.split(":")[0]))
        start_date = start_date.replace(minute=int(start_time_str.split(":")[1]))
        print("Until what time? H:M")
        end_date_str = input()
        end_date = end_date.replace(hour=int(end_date_str.split(":")[0]))
        end_date = end_date.replace(minute=int(end_date_str.split(":")[1]))
        dates_of_interest.append({'start_date': start_date, 'end_date': end_date})
        print("Continue picking dates? (Y, N)")
        if input() != 'Y':
            choosing_dates = False

    user = {
        'email_address': email_address,
        'establishments_of_interest': establishments_of_interest,
        'dates_of_interest': dates_of_interest
    }

    post_user(user)

def get_availabilities_of_interest():
    availabilities = []
    start_date = datetime(2021, 4, 1, 1, 0)
    end_date = datetime(2023, 12, 31, 1, 0)
    establishments = get_establishments_of_interest()
    for establishment in establishments['establishments']:
        place_id = get_establishment_place_id(establishment['id'], establishments)
        service_id = get_place_service_id(place_id, establishments)
        establishment_schedule = get_establishment_schedule(establishment['id'], place_id, service_id, start_date, end_date)
        if 'availabilities' in establishment_schedule:
            availabilities = availabilities + establishment_schedule['availabilities']
    return availabilities

def identify_new_availabilities(updated_availabilities):
    new_availabilities = []
    with open('mock_db/availabilities.json', 'r', encoding='utf-8') as f:
        current_availabilities = json.load(f)
    for availability in updated_availabilities:
        if availability not in current_availabilities:
            new_availabilities.append(availability)
    return new_availabilities

def notify():
    updated_availabilities = get_availabilities_of_interest()
    new_availabilities = identify_new_availabilities(updated_availabilities)
    with open('mock_db/availabilities.json', 'w+', encoding='utf-8') as f:
        json.dump(updated_availabilities, f, ensure_ascii=False, indent=4)

def main():
    # email = 'test@gmail.com'
    # postal_code = 'J4B 6X0'

    # establishments = get_establishments(postal_code)

    # post_establishments(establishments)

    # place_id = get_establishment_place_id(70016)
    # service_id = get_place_service_id(place_id)

    # chosen_places = choose_establishments(0, establishments)

    # days = get_establishment_days(70016, place_id, service_id)

    # schedule = get_establishment_schedule(70016, place_id, service_id, datetime(2021, 4, 4), datetime(2022, 10, 4))

    # user_sign_up()
    notify()


if __name__ == '__main__':
    main()
