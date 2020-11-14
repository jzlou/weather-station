# weather-station

Uses a Raspberry pi, with DHT22 sensor to record data to influx db

# usage

Use tmux via raspberry pi and ssh

1. Modify the python program to capture sensor data from the correct pin on the RPi.
1. Start a tmux session in the pi (`tmux a`)
2. run weather station using python (`python3 thingspeak_main.py`)
3. If you're running a local tmux session, detach the pi session using ctrl+b ctrl+b `d`.
4. All set.
