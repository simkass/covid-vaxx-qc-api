import json

import requests

from api import config


def get_geo_code(postal_code: str):
    url = config.geocode_url_start + postal_code[0:3] + "%20" + postal_code[3:6]
    response = requests.request("GET", url, headers=config.headers, data={})
    return json.loads(response.text)


def get_establishments(postal_code: str, lat: int, lng: int):
    url = config.establishments_url_start + str(lat) + "&longitude=" + str(
        lng) + config.establishments_url_end + postal_code[0:3] + "%20" + postal_code[3:6]
    response = requests.request("GET", url, headers=config.headers, data={})
    return json.loads(response.text)
