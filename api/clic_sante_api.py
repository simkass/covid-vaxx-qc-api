import ast
import json
import requests

def get_establishments(postal_code: str):
    url = "https://api3.clicsante.ca/v3/availabilities?dateStart=2021-04-17&dateStop=2023-08-15&latitude=45.3821028&longitude=-72.7290098&maxDistance=1000&serviceUnified=237&postalCode=" + postal_code[0:3] + "%20" + postal_code[3:6]

    file = open("utils/clic_sante_api_header.txt", "r")
    contents = file.read()
    headers = ast.literal_eval(contents)
    file.close()

    payload={}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)

def get_establishment_days(establishment_id, place_id, service_id):
    url = "https://api3.clicsante.ca/v3/establishments/" + str(establishment_id) + "/schedules/public?dateStart=2021-04-01&dateStop=2021-05-01&service=" + str(service_id) + "&timezone=America/Toronto&places=" + str(place_id) + "&filter1=1&filter2=0"

    payload={}
    file = open("utils/clic_sante_api_header.txt", "r")
    contents = file.read()
    headers = ast.literal_eval(contents)
    file.close()

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)