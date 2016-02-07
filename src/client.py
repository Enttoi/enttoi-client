import sensors
import leds
import time
import RPi.GPIO as GPIO
import os
 
end_point = os.environ["ENTTOI_ENDPOINT"]
client_token = os.environ["ENTTOI_CLIENT_TOKEN"]

GPIO.setmode(GPIO.BCM)

# wPi = 2, 3
doors = [sensors.Sensor(1, 27, "cabin_door"), sensors.Sensor(2, 22, "cabin_door")]

green_indicator = leds.Led(4) # wPi = 7
indicators = [green_indicator]
 
# indicates boot of the client
def boot():
	for i in indicators:
		i.on()

# loops forever on each sensor and sends their state
def start_sending():
	while True:
		for d in doors:
			success = d.send_state(client_token, end_point)	
            		
		time.sleep(0.5)

boot()
start_sending()