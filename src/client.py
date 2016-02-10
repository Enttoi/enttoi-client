import input, output
import RPi.GPIO as GPIO
import datetime, os, sys, threading, requests

CONST_API_TIMEOUT = 3 # after X seconds to timout when calling API
CONST_API_INVOKE_LIMIT = 30 # send updates no more than once in X seconds
CONST_SENSOR_READ_FREQUENCY = 0.2 # cool down between IO reads

# sends data to api and returns success status
def post_to_api(end_point, client_token, payload):
		success = False
		log_message = "{0} Sending {1}:\t".format(
			datetime.datetime.utcnow().strftime("%H:%M:%S"), str(payload))
		
		try:
			r = requests.post(end_point, headers = {'Authorize': client_token}, json = payload, timeout = CONST_API_TIMEOUT)
			log_message += "{0} {1}".format(r.status_code, r.text)
			r.close()
			success = (r.status_code == 200)
		except requests.exceptions.ConnectionError as e:
			log_message += "connection error/timeout waiting for response"
		except requests.exceptions.ConnectTimeout as e:
			log_message += "timeout while connecting"
		except requests.exceptions.ReadTimeout as e:
			log_message += "timeout while getting response"
		except requests.exceptions.HTTPError as e:
			log_message += "HTTP error - {0}".format(e.message)
		except requests.exceptions.RequestException as e:
			log_message += "General error - {0}".format(e.message)
		
		print(log_message)
		return success
		
# loops forever single sensor and reports its state
def process_sensor(door, end_point, client_token, stop_event):
	# send updates no more than once in X seconds
	throttling_factor = datetime.timedelta(0, CONST_API_INVOKE_LIMIT) 
	
	# when the last successful update was sent
	last_request = datetime.datetime.utcnow() - throttling_factor
	
	while (not stop_event.is_set()):
		is_state_changed = door.read_state()
		now = datetime.datetime.utcnow()
		
		if (is_state_changed == True or last_request < (now - throttling_factor)):
			success = post_to_api(end_point, client_token, door.serialize_state(client_token))
			if(success == True):
				last_request = now
			else:
				# force sending current (recently changed) state on next iteration
				last_request = now - throttling_factor
				
		stop_event.wait(CONST_SENSOR_READ_FREQUENCY)	

# spins up thread for each sensor and await interraption 
def main(argv):
	end_point = ""
	client_token = ""
	
	if os.environ.has_key("ENTTOI_ENDPOINT"):
		end_point = os.environ["ENTTOI_ENDPOINT"]
	
	if os.environ.has_key("ENTTOI_CLIENT_TOKEN"):
		client_token = os.environ["ENTTOI_CLIENT_TOKEN"]
		
	if not end_point or not client_token:
		print("Endpoint or/and client token not specified")
		sys.exit(1)
	
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	
	# wPi = 7, 5
	doors = [input.Sensor(1, 4, "cabin_door"), input.Sensor(2, 24, "cabin_door")]
	
	# wPi = 0
	power_indicator = output.Led(17) 

	print("Starting with endpoint [{0}], hit 'Enter' to exit...\n".format(end_point))	
	power_indicator.on()
	
	stop_event = threading.Event()	
	threads = []
	
	for door in doors:
		t = threading.Thread(target=process_sensor, args = (
			door, end_point, client_token, stop_event))
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
	sys.exit(0)
