#!/usr/bin/env python3
"""Simple logging weather station logic"""
import sys
import time
import logging
from datetime import datetime
import Adafruit_DHT
import pika
import json

if len(sys.argv) > 1:
    LOCATION = sys.argv[1]
else:
    LOCATION = 'basement'
logging.info("using %s as location", LOCATION)

CONNECTION = pika.BlockingConnection(pika.ConnectionParameters(
    host='lecole',
    port=5672
))
CHANNEL = CONNECTION.channel()
CHANNEL.queue_declare(queue='scribe')

SENSOR = Adafruit_DHT.DHT22
PIN = 22


def write_point():
    """Writes the point to influx"""
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    logging.info("Recording temp: %s, hum: %s", temperature, humidity)
    if humidity > 100 or humidity < 0:
        raise ValueError("Sensor humidity out of range")
    if temperature > 75 or temperature < 0:
        raise ValueError("Nonsensical value from temperature sensor")
    measurement = {
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
    CHANNEL.basic_publish(exchange='',
                          routing_key='scribe',
                          body=json.dumps(measurement))


while True:
    try:
        write_point()
    except Exception:
        raise RuntimeError("Failed in main loop")
    print("Wrote data to tsdb")
    time.sleep(60)
