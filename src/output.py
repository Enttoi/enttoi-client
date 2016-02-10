import threading, time
import abc
import RPi.GPIO as GPIO

class Led(object):
	
	def __init__(self, pin):
		self.pin = pin
		GPIO.setup(self.pin, GPIO.OUT)
		self.off() # reset state

	def on(self):
		GPIO.output(self.pin,True)

	def off(self):
		GPIO.output(self.pin,False)

