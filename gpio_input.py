﻿"""
Wrappers for INPUT devices connected to GPIO
"""
import datetime
import RPi.GPIO as GPIO


class Sensor(object):
    """Represents reed switch sensor """
    def __init__(self, identity, pin, sensor_type):
        self.identity = identity
        self.__pin = pin
        self.__sensor_type = sensor_type
        self.__last_state = -1
        self.__state_changed_on = datetime.datetime(1979, 5, 30)
        GPIO.setup(self.__pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_state(self):
        """reads the current state of sensor and returns indication whether it changed"""

        new_state = 1 if not GPIO.input(self.__pin) else 0
        if self.__last_state != new_state:
            self.__state_changed_on = datetime.datetime.utcnow()
            print("{0} State changed for pin [{1}] from {2} to {3}".format(
                self.__state_changed_on.strftime("%H:%M:%S"),
                self.__pin, self.__last_state, new_state))
            self.__last_state = new_state
            return True
        else:
            return False

    def serialize_state(self):
        """serialize object for sending over the wire"""

        return {
            "sensorType": self.__sensor_type,
            "sensorId": self.identity,
            "state": self.__last_state}
