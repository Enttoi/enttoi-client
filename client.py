"""
Singleton for performing all workload of the client.
Is initiated from environment - either app.py which executed from shell or from daemon service.
Once an instance created, start() method needs to be called to start the actual monitoring
and then later on stop() to halt.
"""

import datetime
import threading
import requests
import RPi.GPIO as GPIO
import gpio_input
import gpio_output

CONST_API_TIMEOUT = 5  # after X seconds to timout when calling API
CONST_API_INVOKE_LIMIT = 30  # send updates no more than once in X seconds
CONST_SENSOR_READ_FREQUENCY = 0.2  # cool down between IO reads

class Client(object):
    """Defines the client and all operations that can be performed on it"""

    def __init__(self, end_point, client_token):
        if not end_point:
            raise ValueError("'end_point' is required")

        if not client_token:
            raise ValueError("'client_token' is required")

        self.__end_point = end_point
        self.__client_token = client_token

        # send updates no more than once in X seconds
        self.__throttling_factor = datetime.timedelta(
            0, CONST_API_INVOKE_LIMIT)

        # setup GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # wPi = 7, 5
        self.__doors = [gpio_input.Sensor(
            1, 4, "cabin_door"), gpio_input.Sensor(2, 24, "cabin_door")]

        # wPi = 0
        self.__power_indicator = gpio_output.Led(17)

    def start(self):
        """starts client - spins up thread for each sensor and sends data to API"""

        print("Starting client [{0}][{1}]".format(
            CONST_API_TIMEOUT, self.__end_point))
        self.__power_indicator.on()  # indicates no successful post to gateway was done

        self.__stop_event = threading.Event()
        self.__threads = []

        for door in self.__doors:
            thread = threading.Thread(
                target=self.__process_sensor, args=(door,))
            thread.daemon = True
            thread.start()
            self.__threads.append(thread)

    def stop(self):
        """stops client - halts reading sensors and invoking API"""

        try:
            self.__stop_event
        except (NameError, AttributeError):
            print("Client is not running")
        else:
            print("Stopping client...")
            # signal to all threads to stop working
            self.__stop_event.set()

            # wait all threads to finish
            for thread in self.__threads:
                thread.join()

            self.__power_indicator.off()
            print("Client stopped")

    def __process_sensor(self, door):
        """loops forever single sensor and reports its state"""

        # when the last successful update was sent for specific sensor
        last_request = datetime.datetime.utcnow() - self.__throttling_factor

        while not self.__stop_event.is_set():
            is_state_changed = door.read_state()
            now = datetime.datetime.utcnow()

            if is_state_changed or last_request < (now - self.__throttling_factor):
                success = self.__post_to_gateway(door.serialize_state())
                if success:
                    last_request = now
                    self.__power_indicator.blink_slow()  # indicates success
                else:
                    # force sending current (recently changed) state on next
                    # iteration
                    last_request = now - self.__throttling_factor
                    self.__power_indicator.blink_fast()  # indicates error in progress

            self.__stop_event.wait(CONST_SENSOR_READ_FREQUENCY)

    def __post_to_gateway(self, payload):
        """sends data to gateway and returns success status"""
        success = False
        log_message = "{0} Sending {1}:\t".format(
            datetime.datetime.utcnow().strftime("%H:%M:%S"), str(payload))

        try:
            req = requests.post(
                self.__end_point,
                headers={'Authorization': self.__client_token},
                json=payload,
                timeout=CONST_API_TIMEOUT)
            log_message += "{0} {1}".format(req.status_code, req.text)

            req.close()
            success = (req.status_code == 200)
        except requests.exceptions.ConnectionError as exc:
            log_message += "connection error/timeout waiting for response - {0}".format(exc)
        except requests.exceptions.ReadTimeout as exc:
            log_message += "timeout while getting response - {0}".format(exc)
        except requests.exceptions.HTTPError as exc:
            log_message += "HTTP error - {0}".format(exc)
        except requests.exceptions.RequestException as exc:
            log_message += "General error - {0}".format(exc)

        print(log_message)
        return success
