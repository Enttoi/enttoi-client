import sensors
import leds
import time
import RPi.GPIO as GPIO
import os
import threading
 
end_point = os.environ["ENTTOI_ENDPOINT"]
client_token = os.environ["ENTTOI_CLIENT_TOKEN"]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# wPi = 4
doors = [sensors.Sensor(1, 23, "cabin_door"), sensors.Sensor(2, 24, "cabin_door")]

# wPi = 0
power_indicator = leds.Led(17) 

# loops forever single sensor and reports its state
def read_send(door, stop_event):	
	while (not stop_event.is_set()):
		state_changed = door.read_state()
		# meantime send anyway (even if state didn't change)
		success = door.send_state(client_token, end_point)
		stop_event.wait(0.5)	

# spins up thread for each sensor and await interraption 
def start():
	t_stop = threading.Event()	
	
	for d in doors:
		t = threading.Thread(target=read_send, args = (d, t_stop))
		t.daemon = True
		t.start()
	
	try:
		# block main thread
		raw_input("Started, hit 'Enter' to exit...")	
	except KeyboardInterrupt:
		pass
		
	# signal to all threads to stop working
	t_stop.set()

power_indicator.on()
start()
power_indicator.off()
		