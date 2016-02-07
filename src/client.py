import sensors
import leds
import time
import RPi.GPIO as GPIO
import os
 
end_point = os.environ["ENTTOI_ENDPOINT"]
client_token = os.environ["ENTTOI_CLIENT_TOKEN"]

GPIO.setmode(GPIO.BCM)

# wPi = 4
doors = [sensors.Sensor(1, 23, "cabin_door")]

# wPi = 0
green_indicator = leds.Led(17) 

# loops forever on each sensor and sends their state
def start_sending():
	green_indicator.on()
	try:
		while True:
			for d in doors:
				state_changed = d.read_state()
				# meantime send anyway (even if state didn't change)
				success = d.send_state(client_token, end_point)
			time.sleep(0.5)
	except KeyboardInterrupt:
		green_indicator.off()
		pass

start_sending()