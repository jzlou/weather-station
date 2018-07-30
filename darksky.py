#!/usr/bin/python3
'''
get hourly data from darksky
'''

import os
import json
from time import time
import requests

DARKSKY_URL = "https://api.darksky.net/forecast/"
DARKSKY_TOKEN = os.environ["DARKSKY_TOKEN"]
LAT_LONG = os.environ["LAT_LONG"]

def get_datasets():
    """
    test
    """
    url = DARKSKY_URL + DARKSKY_TOKEN + "/" + LAT_LONG + "," + int(time())
    response = requests.get(url)
    resp_json = response.json()
    print(json.dumps(resp_json, indent=2))

if __name__ == "__main__":
    get_datasets()
