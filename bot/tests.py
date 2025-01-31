import json
import requests
import uuid
import random

def check_imei():
    url = 'https://api.imeicheck.net/v1/checks'

    token = 'e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b'

    # Add necessary headers
    headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
    }

    # Add body
    body =  json.dumps({
    "deviceId": "356735111052198",
    "serviceId": 12
    })

    # Execute request
    response = requests.post(url, headers=headers, data=body)

    print(response.text)
    
check_imei()

 # Base URL
def check_servises():
    url = 'https://api.imeicheck.net/v1/services'

    token = 'VL4XgpGsaafVecqGYzxCZlG34kZlQn9y5xbk03h4c1844760'

    # Add necessary headers
    headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
    }

    # Execute request
    response = requests.get(url, headers=headers)

    print(response.text)
    
check_servises()