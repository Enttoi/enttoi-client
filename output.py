"""Wrappers for OUTPUT devices connected to GPIO"""
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
		self.__ensure_not_blinking()
		GPIO.output(self.pin,True)

	def off(self):
		self.__ensure_not_blinking()
		GPIO.output(self.pin,False)
		
	def blink_fast(self):
		self.blink(0.07)

	def blink_slow(self):
		self.blink(0.3)
		
	def blink(self, frequency):
		self.__ensure_not_blinking()
		self.__stop_blink_event = threading.Event()	
		self.__thread = threading.Thread(target=self.__do_blinking, args = (frequency,))
		self.__thread.daemon = True
		self.__thread.start()
	
	def __do_blinking(self, frequency):
		state = False;
		GPIO.output(self.pin, state)
	
		while (not self.__stop_blink_event.is_set()):
			state = not state
			GPIO.output(self.pin,state)
			self.__stop_blink_event.wait(frequency)
			
	def __ensure_not_blinking(self):
		try:
			self.__stop_blink_event
		except (NameError, AttributeError):
			pass
		else:
			self.__stop_blink_event.set()
			self.__thread.join()