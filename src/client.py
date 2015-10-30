import sensors
import leds
import time
import RPi.GPIO as GPIO
 
end_point = ""
client_token = ""
GPIO.setmode(GPIO.BCM)

doors = [sensors.Sensor(1, 23, "cabin_door"), sensors.Sensor(2, 26, "cabin_door")]
red_indicator = leds.Led(4)
green_indicator = leds.Led(17)
yellow_indicator = leds.Led(18)
indicators = [red_indicator, green_indicator, yellow_indicator]
 
# indicates boot of the client
def boot():
	for i in indicators:
		i.on()
	time.sleep(1) 
	for i in indicators:
		i.off()

# loops forever on each sensor and sends their state
def start_sending():
	while True:
		for d in doors:
			yellow_indicator.on()
			success = d.send_state(client_token, end_point)		
				
			for i in indicators:
				i.off()
			if(success == False):
				red_indicator.on()
			else:
				green_indicator.on()
		
		time.sleep(0.5)

boot()
start_sending()