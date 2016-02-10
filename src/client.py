import sensors, leds
import datetime, os, sys, threading
import RPi.GPIO as GPIO

# loops forever single sensor and reports its state
def read_send(door, throttling_factor, frequency, end_point, client_token, stop_event):	
	# when the last successful update was sent
	last_request = datetime.datetime.utcnow() - throttling_factor
	
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
				
		stop_event.wait(frequency)	

# spins up thread for each sensor and await interraption 
def main(argv):
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

	print("Starting with endpoint [{0}], hit 'Enter' to exit...\n".format(end_point))	
	power_indicator.on()
	
	stop_event = threading.Event()	
	threads = []
	
	for door in doors:
		t = threading.Thread(target=read_send, args = (
			door, throttling_factor, 0.2, end_point, client_token, stop_event))
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
	stop_event.set()
	
	# wait all threads to finish
	for t in threads:
		t.join()
		
	power_indicator.off()

if __name__ == "__main__":
   main(sys.argv[1:])		
