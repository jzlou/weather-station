#!/usr/bin/python3
'''
get hourly data from NOAA
'''

import os
import json
import requests

NOAA_URL = "https://www.ncdc.noaa.gov/cdo-web/api/v2/"
NOAA_TOKEN = os.environ["NOAA_TOKEN"]

def get_datasets():
    """
    test
    """
    url = NOAA_URL + "stations"
    headers = {"token": NOAA_TOKEN}
    response = requests.get(url, headers=headers)
    resp_json = response.json()
    print(json.dumps(resp_json, indent=2))

if __name__ == "__main__":
    get_datasets()
