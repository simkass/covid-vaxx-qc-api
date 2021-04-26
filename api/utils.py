from datetime import datetime

from dateutil import tz

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')


def get_datetime(date_str, convert_from_utc=False):
    date_time = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
    if convert_from_utc:
        datetime_utc = date_time.replace(tzinfo=from_zone)
        return datetime_utc.astimezone(to_zone)
    return date_time


def get_datetime_strings(date_str):
    date_time = get_datetime(date_str)
    return date_time.strftime("%m/%d/%Y"), date_time.strftime("%H:%M:%S")


def identify_new_availabilities(previous_availabilities, current_availabilities):
    new_availabilties = []
    for availability in current_availabilities:
        previous = next((a for a in previous_availabilities if a['id'] == availability['id']), None)
        if previous is None:
            new_availabilties.append(availability)
    return new_availabilties


def identify_availabilities_of_interest(current_availabilities, user):
    availabilities_of_interest = []

    user_start = get_datetime(user['availabilities']['start'], True)
    user_stop = get_datetime(user['availabilities']['stop'], True)

    for availability in current_availabilities:
        start = get_datetime(availability['start'], True)
        if user_start <= start <= user_stop and availability['place'] in user['establishments_of_interest']:
            availabilities_of_interest.append(availability)

    return availabilities_of_interest
