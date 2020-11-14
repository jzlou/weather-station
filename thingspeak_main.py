#!/usr/bin/env python3
"""Simple logging weather station logic"""
from datetime import datetime
import time
import Adafruit_DHT
import os
import requests
from dotenv import load_dotenv
load_dotenv()


location = os.getenv("LOCATION")
print(f"using {location} as location",)

api_key = os.getenv("THINGSPEAK_API_KEY")
base_url = os.getenv("THINGSPEAK_URI")

SENSOR = Adafruit_DHT.DHT22
PIN = os.getenv("DHT_PIN")


def write_point_wait():
    """Writes the point to influx"""
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    if humidity is None or temperature is None:
        print("received invalid measurement (None)")
        return
    if humidity > 100 or humidity < 0:
        print("Sensor humidity out of range", humidity)
        return
    if temperature > 100 or temperature < 0:
        print("Nonsensical value from temperature sensor", temperature)
        return

    temperature = temperature * 1.8 + 32
    print(f"Recording temp: {temperature}, hum: {humidity}",)

    url = base_url + api_key + f"&field1={temperature}&field2={humidity}"
    r = requests.get(url)
    print(f"Status code: {r.status_code}")

    time.sleep(3 * 60)


if __name__ == "__main__":
    while True:
        try:
            write_point_wait()
        except Exception:
            raise RuntimeError("Failed in main loop")
