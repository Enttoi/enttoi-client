#!/usr/bin/env python
"""Main entry point to application when running client from daemon"""

import logging
import logging.handlers
import sys
import signal
import time
import os
import client

# Deafults
LOG_FILENAME = "/tmp/entoi-client.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class EnttoiLogger(object):
	def __init__(self, logger, level):
		self.logger = logger
		self.level = level

	def write(self, message):
		# Only log if there is a message (not just a new line)
		if message.rstrip() != "":
			self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO and ERROR level
sys.stdout = EnttoiLogger(logger, logging.INFO)
sys.stderr = EnttoiLogger(logger, logging.ERROR)

# get configuration of gateway
end_point = ""
client_token = ""

if os.environ.has_key("ENTTOI_ENDPOINT"):
	end_point = os.environ["ENTTOI_ENDPOINT"]

if os.environ.has_key("ENTTOI_CLIENT_TOKEN"):
	client_token = os.environ["ENTTOI_CLIENT_TOKEN"]
	
if not end_point or not client_token:
	print("Endpoint or/and client token not specified")
	sys.exit(1)

# start client and handle stop
c = client.Client(end_point, client_token)
c.start()
		
def signal_term_handler(signal, frame):
	c.stop()
	sys.exit(0)
	
signal.signal(signal.SIGTERM, signal_term_handler)

# block main thread 
while True:
	time.sleep(1)