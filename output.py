﻿"""Wrappers for OUTPUT devices connected to GPIO"""
import abc
import threading
import RPi.GPIO as GPIO

CONST_BLINK_FREQUENCY = 0.07
	
class Led(object):

	
	def __init__(self, pin):
		self.pin = pin
		GPIO.setup(self.pin, GPIO.OUT)
		self.off() # reset state

	def on(self):
		self.__ensureNotBlinking()
		GPIO.output(self.pin,True)

	def off(self):
		self.__ensureNotBlinking()
		GPIO.output(self.pin,False)

	def blink(self):
		self.__ensureNotBlinking()
		self.__stop_blink_event = threading.Event()	
		self.__thread = threading.Thread(target=self.__doBlinking)
		self.__thread.daemon = True
		self.__thread.start()
		
	def __doBlinking(self):
		state = False;
		GPIO.output(self.pin, state)
	
		while (not self.__stop_blink_event.is_set()):
			state = not state					
			GPIO.output(self.pin,state)
			self.__stop_blink_event.wait(CONST_BLINK_FREQUENCY)
			
	def __ensureNotBlinking(self):
		try:
			self.__stop_blink_event
		except (NameError, AttributeError):
			pass
		else:
			self.__stop_blink_event.set()
			self.__thread.join()