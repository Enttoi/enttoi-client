import abc
import datetime
import requests
import random

class Sensor(object):
	
	def __init__(self, identity, pin, sensor_type):
		self.identity = identity
		self.__pin = pin
		self.__sensor_type = sensor_type
		self.__last_state = 0
		self.__state_changed_on = datetime.datetime(1979, 1, 1, 0, 0, 0, 0)
	
	# reads the current state of sensor
	def __read_state(self):
		self.__last_state = 1 if random.random() > 0.9 else 0

	# reads and sends the current state of sensor
	def send_state(self, client_token, end_point):
		success = False
		self.__read_state()

		payload = {"token": client_token, "sensorType": self.__sensor_type, "sensorId": self.identity, "state": self.__last_state}

		print("Payload:\t{0}".format(str(payload)))	
		try:
			r = requests.post(end_point, json=payload)
			print("Response:\t{0} {1}".format(r.status_code, r.text))
			r.close()
			success = (r.status_code == 200)
		except requests.exceptions.ConnectionError as e:
			print("Error:\tconnection error")
		except requests.exceptions.ConnectTimeout as e:
			print("Error:\ttimeout while connecting")
		except requests.exceptions.ReadTimeout as e:
			print("Error:\ttimeout while getting response")
		except requests.exceptions.HTTPError as e:
			print("HTTP error:\t{0}".format(e.message))	
		except requests.exceptions.RequestException as e:
			print("General error:\t{0}".format(e.message))
		print("")	

		return success