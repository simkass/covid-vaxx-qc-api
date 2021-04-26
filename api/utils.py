from datetime import datetime

from dateutil import tz

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')


def get_datetime(date_str):
    date_time = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
    datetime_utc = date_time.replace(tzinfo=from_zone)
    return datetime_utc.astimezone(to_zone)


def get_datetime_strings(date_str):
    date_time = get_datetime(date_str)
    return date_time.strftime("%m/%d/%Y"), date_time.strftime("%H:%M:%S")
