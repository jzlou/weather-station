#!/usr/bin/env python3
"""Simple logging weather station logic"""
from datetime import datetime
import time
import Adafruit_DHT
import os
import requests
from dotenv import load_dotenv
load_dotenv()


sleep_interval = 3 * 60
exception_interval = 60 * 60
location = os.getenv("LOCATION")
print(f"using {location} as location")

api_key = os.getenv("THINGSPEAK_API_KEY")
base_url = os.getenv("THINGSPEAK_URI")

SENSOR = Adafruit_DHT.DHT22
PIN = os.getenv("DHT_PIN")


def write_point_wait():
    """Writes the point to influx"""
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    if humidity is None or temperature is None:
        print("Received invalid measurement: None")
        return False
    if humidity > 100 or humidity < 0:
        print("Sensor humidity out of range:", humidity)
        return False
    if temperature > 100 or temperature < 0:
        print("Nonsensical value from temperature sensor:", temperature)
        return False

    temperature_f = temperature * 1.8 + 32
    print(f"Measured: {temperature_f}, hum: {humidity}",)
    return f"&field1={temperature_f}&field2={humidity}"


if __name__ == "__main__":
    while True:
        try:
            write_string = write_point_wait()
            if write_string:
                url = base_url + api_key + write_string
                r = requests.get(url)
                print(f"Write attempt status code: {r.status_code}")
            time.sleep(sleep_interval)
        except Exception:
            # if things go sideways, try again later
            time.sleep(exception_interval)
