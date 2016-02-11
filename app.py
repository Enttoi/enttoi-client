import os, sys, client

def main(argv):
	end_point = ""
	client_token = ""
	
	if os.environ.has_key("ENTTOI_ENDPOINT"):
		end_point = os.environ["ENTTOI_ENDPOINT"]
	
	if os.environ.has_key("ENTTOI_CLIENT_TOKEN"):
		client_token = os.environ["ENTTOI_CLIENT_TOKEN"]
		
	if not end_point or not client_token:
		print("Endpoint or/and client token not specified")
		sys.exit(1)
		
	c = client.Client(end_point, client_token)
	print("Hit 'Enter' or 'Ctr+C' to exit...\n")
	
	c.start()
	try:
		# block main thread
		raw_input("")	
	except KeyboardInterrupt:
		pass
		
	c.stop()
	
if __name__ == "__main__":
	main(sys.argv[1:])
	sys.exit(0)