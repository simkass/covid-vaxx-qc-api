import json

import requests

from api import config


def get_geo_code(postal_code: str):
    url = config.geocode_url_start + postal_code[0:3] + "%20" + postal_code[3:6]
    response = requests.request("GET", url, headers=config.headers, data={})
    return json.loads(response.text)


def get_establishments(postal_code, lat, lng):
    page = 0
    establishments_full = {"establishments": [], "places": [], "distanceByPlaces": {}, "serviceIdsByPlaces": []}

    while(page < 5):
        url = config.establishments_url_start + str(lat) + "&longitude=" + str(
            lng) + config.establishments_url_end + postal_code[0:3] + "%20" + postal_code[3:6] + "&page=" + str(page)
        response = requests.request("GET", url, headers=config.headers, data={})

        if response.text != '':
            establishments = json.loads(response.text)
            establishments_full = merge_establishments(establishments_full, establishments)
            page += 1
        else:
            page = 5

    return establishments_full


def merge_establishments(est1, est2):
    est1['distanceByPlaces'].update(est2['distanceByPlaces'])
    return {"establishments": est1['establishments'] + est2['establishments'],
            "places": est1['places'] + est2['places'],
            "distanceByPlaces": est1['distanceByPlaces'], "serviceIdsByPlaces": []}


def get_establishment_service(establishment_id):
    url = config.establishments_service_url + str(establishment_id) + "/services"
    response = requests.request("GET", url, headers=config.headers, data={})
    service = None
    if response.status_code == 200:
        response = json.loads(response.text)
        service = next((service for service in response if service['service_template']['id'] in [126, 159]), None)
    if service is not None:
        return service['id']
    return 0


def get_availabilities(establishments):
    availabilities = []

    for establishment in establishments:
        service = get_establishment_service(establishment['establishment'])
        url = config.availabilities_url_start + str(establishment['establishment']) + config.availabilities_url_mid + \
            str(service) + config.availabilities_url_last + str(establishment['id']) + "&filter1=1&filter2=0"
        response = requests.request("GET", url, headers=config.headers, data={})
        if response.status_code == 200:
            availabilities = availabilities + json.loads(response.text)['availabilities']

    return availabilities