import sensors
import time
import requests
import random
 
end_point = "http://enttoigw.azurewebsites.net/sensor"
client_token = "e997b810-f0ae-4cde-b933-e2ed6430d2d1"
doors = [sensors.Sensor(1, 23, "cabin_door"), sensors.Sensor(2, 26, "cabin_door")]
 
while True:
	for d in doors:
		# TODO: read GPIO here
		d.last_state = 1 if random.random() > 0.9 else 0
		
		# send state
		payload = {"token": client_token, "sensorType": d.sensor_type, "sensorId": d.identity, "state": d.last_state}
				
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
			print("Error:\t{0}".format(e.message))	
		
		print("")	
		
	time.sleep(0.5)