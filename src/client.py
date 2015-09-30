import door
import time
import requests
import random
 
end_point = "http://enttoigw.azurewebsites.net/status"
room_token = 1 # TODO: change to GUID "e997b810-f0ae-4cde-b933-e2ed6430d2d1"
doors = [door.Door(1, 23), door.Door(2, 26)]
 
while True:
	for d in doors:
		# TODO: read GPIO here
		d.last_state = 1 if random.random() > 0.9 else 0
		
		# send state
		# TODO: send real state
		payload = {"room": room_token, "door": d.identity, "state": d.last_state}
		
		print("Payload:\t{0}".format(str(payload)))	
		r = requests.post(end_point, data=payload)
		print("Response:\t{0} {1}\n".format(r.status_code, r.text))	
		r.close()
		
	time.sleep(0.5)