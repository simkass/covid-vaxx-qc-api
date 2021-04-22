auth_token = ''

headers = {
    'authority': 'api3.clicsante.ca',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'accept': 'application/json, text/plain, */*',
    'authorization': 'Basic ' + auth_token,
    'x-trimoz-role': 'public',
    'sec-ch-ua-mobile': '?0',
    'product': 'clicsante',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'origin': 'https://clients3.clicsante.ca',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://clients3.clicsante.ca/',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8',
    'cookie': '_ga=GA1.2.914255478.1617718370; _gid=GA1.2.1118002748.1618588676; privacyConsent=1; _gat=1; PHPSESSID=4c629fd3dbe288ba6617bb67e93668f0'
}

geocode_url_start = 'https://api3.clicsante.ca/v3/geocode?address='

establishments_url_start = "https://api3.clicsante.ca/v3/availabilities?dateStart=2021-04-17&dateStop=2023-08-15&latitude="
establishments_url_end = "&maxDistance=40&serviceUnified=237&postalCode="
