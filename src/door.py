import datetime

class Door(object):
	
	def __init__(self, identity, pin):
		self.identity = identity
		self.pin = pin
		self.last_state = 0
		self.state_changed_on = datetime.datetime(1979, 1, 1, 0, 0, 0, 0)