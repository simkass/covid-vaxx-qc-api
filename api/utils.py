from datetime import datetime

from dateutil import tz

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')

# Months, there has to be a better way to do this
months = {"01": "janvier", "02": "février", "03": "mars", "04": "avril", "05": "mai", "06": "juin",
          "07": "juillet", "08": "aout", "09": "septembre", "10": "octobre", "11": "novembre", "12": "décembre"}


def get_datetime(date_str, convert_from_utc=False):
    date_time = datetime.strptime(date_str[0:16], "%Y-%m-%dT%H:%M")
    if convert_from_utc:
        datetime_utc = date_time.replace(tzinfo=from_zone)
        return datetime_utc.astimezone(to_zone)
    return date_time.replace(tzinfo=to_zone)


def get_datetime_strings(date_str):
    date_time = get_datetime(date_str)
    return date_time.strftime("%m/%d/%Y"), date_time.strftime("%H:%M")


def get_datetime_full_strings(date_str):
    date, time = get_datetime_strings(date_str)
    date_full_string = date[3:5].replace("0", "") + " " + months.get(date[0:2]) + " " + date[6:12]
    return date_full_string, time


def identify_new_availabilities(previous_availabilities, current_availabilities):
    new_availabilties = []
    for availability in current_availabilities:
        previous = next((a for a in previous_availabilities if a['id'] == availability['id']), None)
        if previous is None:
            new_availabilties.append(availability)
    return new_availabilties


def identify_availabilities_of_interest(current_availabilities, user):
    availabilities_of_interest = []

    for availability in current_availabilities:
        start = get_datetime(availability['start'], True)
        a = next((a for a in user['availabilities'] if get_datetime(
            a['start']) <= start <= get_datetime(a['stop'])), None)

        if a is not None and availability['place'] in user['establishments_of_interest']:
            availabilities_of_interest.append(availability)

    return availabilities_of_interest
