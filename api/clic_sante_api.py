import json

import requests

from api import config


def get_establishments(postal_code: str):
    postal_code = postal_code.replace(" ", "")
    url = config.get_establishments_url_start + postal_code[0:3] + "%20" + postal_code[3:6]
    response = requests.request("GET", url, headers=config.headers, data={})
    return json.loads(response.text)
