#!/usr/bin/python3
'''
Interact with darksky API
'''

import os
from time import time
import asyncio
import requests

DARKSKY_URL = "https://api.darksky.net/forecast/"
DARKSKY_TOKEN = os.environ["DARKSKY_TOKEN"]
LAT_LONG = os.environ["LAT_LONG"]

async def async_query(t_epoch, excludes=None):
>>>>>>> wip, save
    """
    Query darksky API for data and respond asynchronously

    :param t_epoch: (int) seconds since epoch
    :param excludes: (list<string>) list of exclude blocks
    :return: (json) response
    """
    url = DARKSKY_URL + DARKSKY_TOKEN + "/" + LAT_LONG + "," + str(t_epoch)
    if excludes:
        url += "?excludes="
        for exclude in excludes:
            url += exclude
    await requests.get(url).json()

def query(t_epoch, excludes=None):
    """
    Query darksky API for data

    :param t_epoch: (int) seconds since epoch
    :param excludes: (list<string>) list of exclude blocks
    :return: (json) response
    """
    url = DARKSKY_URL + DARKSKY_TOKEN + "/" + LAT_LONG + "," + str(t_epoch)
    if excludes:
        url += "?excludes="
        for exclude in excludes:
            url += exclude
    return requests.get(url).json()


if __name__ == "__main__":
    print(query(int(time()))["minutely"]["summary"])
