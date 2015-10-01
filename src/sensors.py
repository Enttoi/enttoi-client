import abc
import datetime

class Sensor(object):
	
	def __init__(self, identity, pin, sensor_type):
		self.identity = identity
		self.pin = pin
		self.sensor_type = sensor_type
		self.last_state = 0
		self.state_changed_on = datetime.datetime(1979, 1, 1, 0, 0, 0, 0)