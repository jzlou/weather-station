import sys
import time
from datetime import datetime
from influxdb import InfluxDBClient
import Adafruit_DHT

if sys.argv:
    LOCATION = sys.argv[0]
else:
    LOCATION = 'basement'
print("using", LOCATION, "as location")

CLIENT = InfluxDBClient(host="localhost", port=8086)
CLIENT.switch_database("weather")

SENSOR = Adafruit_DHT.DHT22
PIN = 22

def write_point():
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    print("Temperature:", temperature, "Humidity:", humidity)
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
    write_point()
    print("Wrote data to tsdb")
    time.sleep(60)
