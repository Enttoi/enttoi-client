import sensors
import leds
import time
import requests
import random
import RPi.GPIO as GPIO
 
end_point = ""
client_token = ""
GPIO.setmode(GPIO.BCM)

doors = [sensors.Sensor(1, 23, "cabin_door"), sensors.Sensor(2, 26, "cabin_door")]
indicators = [leds.Led(1, 17, "green")]
 
# indicates boot of the client
def boot():
    for i in indicators:
            i.on()
    time.sleep(3) 
    for i in indicators:
            i.off()

# sends a specified sensor's state
def send_sensor(sensor):
     # TODO: read GPIO here
    sensor.last_state = 1 if random.random() > 0.9 else 0

    # send state
    payload = {"token": client_token, "sensorType": sensor.sensor_type, "sensorId": sensor.identity, "state": sensor.last_state}

    print("Payload:\t{0}".format(str(payload)))	
    try:
        r = requests.post(end_point, json=payload)
        print("Response:\t{0} {1}".format(r.status_code, r.text))
        r.close()
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

# loops forever on each sensor and sends their state
def start_sending():
    while True:
        for d in doors:
            send_sensor(d)
        time.sleep(0.5)

boot()
start_sending()