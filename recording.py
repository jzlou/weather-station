#!/usr/bin/env python3
"""Simple logging weather station logic"""
import sys
import time
import logging
from datetime import datetime
from influxdb import InfluxDBClient
import Adafruit_DHT

if len(sys.argv) > 1:
    LOCATION = sys.argv[1]
else:
    LOCATION = 'basement'
logging.info("using", LOCATION, "as location")

CLIENT = InfluxDBClient(host="localhost", port=8086)
CLIENT.switch_database("weather")

SENSOR = Adafruit_DHT.DHT22
PIN = 22

def write_point():
    """Writes the point to influx"""
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    logging.info("Recording temp:", temperature, "hum:", humidity)
    measurement_json = [
        {
            "measurement": "weather",
            "tags": {
                "location": LOCATION
                },
            "time": datetime.now(),
            "fields": {
                "humidity": humidity,
                "temperature": temperature
                }
            }
        ]
    CLIENT.write_points(measurement_json)

while True:
    try:
        write_point()
    except:
        logging.warning("Something bad happened at", datetime.now().toString())
    print("Wrote data to tsdb")
    time.sleep(60)
