import sensors
import leds
import datetime
import RPi.GPIO as GPIO
import os
import threading
 
end_point = os.environ["ENTTOI_ENDPOINT"]
client_token = os.environ["ENTTOI_CLIENT_TOKEN"]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# wPi = 7, 5
doors = [sensors.Sensor(1, 4, "cabin_door"), sensors.Sensor(2, 24, "cabin_door")]

# wPi = 0
power_indicator = leds.Led(17) 

# send updates no more than once in X seconds
throttling_factor = datetime.timedelta(0, 30) 

# loops forever single sensor and reports its state
def read_send(door, stop_event):	
	
	# when the last successful update was sent
	last_request = datetime.datetime(1979, 1, 1, 0, 0, 0, 0) 
	
	while (not stop_event.is_set()):
		is_state_changed = door.read_state()
		now = datetime.datetime.utcnow()
		
		if (is_state_changed == True or last_request < (now - throttling_factor)):
			success = door.send_state(client_token, end_point)
			if(success == True):
				last_request = now
			else:
				# force sending current (recently changed) state on next iteration
				last_request = now - throttling_factor
				
		stop_event.wait(0.5)	

# spins up thread for each sensor and await interraption 
def start():
	print("Starting with endpoint [{0}], hit 'Enter' to exit...\n".format(end_point))	
	
	t_stop = threading.Event()	
	threads = []
	
	for d in doors:
		t = threading.Thread(target=read_send, args = (d, t_stop))
		t.daemon = True
		t.start()
		threads.append(t)
		
	try:
		# block main thread
		raw_input("")	
	except KeyboardInterrupt:
		pass
		
	print("Exiting...")	
	# signal to all threads to stop working
	t_stop.set()
	
	# wait all threads to finish
	for t in threads:
		t.join()
		
power_indicator.on()
start()
power_indicator.off()
		