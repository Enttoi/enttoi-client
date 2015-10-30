import abc
import RPi.GPIO as GPIO

class Led(object):
	
	def __init__(self, identity, pin, color):
		self.identity = identity
		self.pin = pin
		self.color = color
		GPIO.setup(self.pin, GPIO.OUT)
		self.off() # reset state

	def on(self):
		GPIO.output(self.pin,True)

	def off(self):
		GPIO.output(self.pin,False)