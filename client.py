"""
Singleton for performing all workload of the client
Is initiated from environment - either app.py which executed 
from shell or from daemon service. Once an instance created,
start() method needs to be called to start the actual monitoring
and then later on stop() to halt.
"""

import input, output
import RPi.GPIO as GPIO
import datetime, threading, requests

CONST_API_TIMEOUT = 5 # after X seconds to timout when calling API
CONST_API_INVOKE_LIMIT = 30 # send updates no more than once in X seconds
CONST_SENSOR_READ_FREQUENCY = 0.2 # cool down between IO reads

class Client(object):
	
	def __init__(self, end_point, client_token):
		if not end_point:
			raise ValueError("'end_point' is required")
			
		if not client_token:
			raise ValueError("'client_token' is required")
			
		self.__end_point = end_point
		self.__client_token = client_token
		
		# send updates no more than once in X seconds
		self.__throttling_factor = datetime.timedelta(0, CONST_API_INVOKE_LIMIT) 
		
		# setup GPIO
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		
		# wPi = 7, 5
		self.__doors = [input.Sensor(1, 4, "cabin_door"), input.Sensor(2, 24, "cabin_door")]
		
		# wPi = 0
		self.__power_indicator = output.Led(17) 
		
	# starts client - spins up thread for each sensor and sends data to API 
	def start(self):
		print("Starting client [{0}][{1}]".format(CONST_API_TIMEOUT, self.__end_point))	
		self.__power_indicator.blink()	# indicates no successful post to gateway was done
		
		self.__stop_event = threading.Event()	
		self.__threads = []
		
		for door in self.__doors:
			thread = threading.Thread(target=self.__process_sensor, args = (door,))
			thread.daemon = True
			thread.start()
			self.__threads.append(thread)
			
	# stops client - halts reading sensors and invoking API 
	def stop(self):		
		try:
			self.__stop_event
		except (NameError, AttributeError):
			print "Client is not running"
		else:
			print("Stopping client...")
			# signal to all threads to stop working
			self.__stop_event.set()
			
			# wait all threads to finish
			for thread in self.__threads:
				thread.join()
				
			self.__power_indicator.off()
			print("Client stopped")		

	# loops forever single sensor and reports its state
	def __process_sensor(self, door):
		
		# when the last successful update was sent for specific sensor
		last_request = datetime.datetime.utcnow() - self.__throttling_factor
		
		while (not self.__stop_event.is_set()):
			is_state_changed = door.read_state()
			now = datetime.datetime.utcnow()
			
			if (is_state_changed or last_request < (now - self.__throttling_factor)):
				success = self.__post_to_gateway(door.serialize_state())
				if(success):
					last_request = now
					self.__power_indicator.on() # indicates success
				else:
					# force sending current (recently changed) state on next iteration
					last_request = now - self.__throttling_factor
					self.__power_indicator.blink() # indicates error in progress
					
			self.__stop_event.wait(CONST_SENSOR_READ_FREQUENCY)	
		
	# sends data to gateway and returns success status
	def __post_to_gateway(self, payload):
			success = False
			log_message = "{0} Sending {1}:\t".format(
				datetime.datetime.utcnow().strftime("%H:%M:%S"), str(payload))
			
			try:
				r = requests.post(
					self.__end_point, 
					headers = {'Authorization': self.__client_token}, 
					json = payload, 
					timeout = CONST_API_TIMEOUT)
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
		
