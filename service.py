#!/usr/bin/env python
"""Main entry point to application when running client from daemon"""

import logging, logging.handlers, argparse, sys

# Deafults
LOG_FILENAME = "/tmp/entoi-client.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="Enttoi client service")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
	LOG_FILENAME = args.log

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

# Replace stdout with logging to file at INFO level
sys.stdout = EnttoiLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = EnttoiLogger(logger, logging.ERROR)

# Loop forever, doing something useful hopefully:
# while True:
#         logger.info("The counter is now " + str(i))
#         print "This is a print"
#         i += 1
#         time.sleep(5)
#         if i == 3:
#                 j = 1/0  # cause an exception to be thrown and the program to exit