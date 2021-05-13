from api import config

import requests
import json

valid_postal_code = 'J8E%200A1'
valid_establishment_id = '74616'
valid_longitude = '-74.568391199999994'
valid_latitude = '46.1322197'
valid_service_id = '6219'
valid_place_id = '5873'

url_geocode = config.geocode_url_start + 'J8E%200A1'
url_establishments = config.establishments_url_start + valid_latitude + "&longitude=" + \
                     valid_longitude + config.establishments_url_end + valid_postal_code + '&page=0'
url_availabilities = config.availabilities_url_start + valid_establishment_id + config.availabilities_url_mid + \
                     valid_service_id + config.availabilities_url_last + valid_place_id + "&filter1=1&filter2=0"
url_services = config.establishments_service_url + valid_establishment_id + "/services"

response_geocode = requests.request("GET", url_geocode, headers=config.headers, data={})
response_establishments = requests.request("GET", url_establishments, headers=config.headers, data={})
response_availabilities = requests.request("GET", url_availabilities, headers=config.headers, data={})
response_services = requests.request("GET", url_services, headers=config.headers, data={})


def test_validate_active_routes():
    assert response_geocode.status_code == 200, 'Request geocode has been denied'
    assert response_establishments.status_code == 200, 'Request establishments has been denied'
    assert response_availabilities.status_code == 200, 'Request availabilities has been denied'
    assert response_services.status_code == 200, 'Request services has been denied'


def test_validate_geocode_route():
    value = json.loads(response_geocode.text)
    assert 'results' in value, 'Geocode no longer has results key'
    assert len(value['results']) > 0, 'Geocode result is empty'
    assert 'geometry' in value['results'][0], 'Geocode no longer has geometry key'
    assert 'location' in value['results'][0]['geometry'], 'Geocode no longer has location key'


def test_validate_establishment_route():
    value = json.loads(response_establishments.text)
    assert 'establishments' in value, 'Establishment no longer has establishments key'
    assert 'places' in value, 'Establishment no longer has places key'


def test_validate_availabilities_route():
    value = json.loads(response_availabilities.text)
    assert 'availabilities' in value, 'Availabilities no longer has availabilities key'


def test_validate_service_route():
    value = json.loads(response_services.text)
    assert len(value) > 0, 'Service result is empty'
    assert 'service_template' in value[0], 'Service no longer has service_template key'
    assert 'id' in value[0]['service_template'], 'Service no longer has id key'
