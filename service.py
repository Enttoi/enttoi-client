#!/usr/bin/env python
"""Main entry point to application when running client from daemon"""

import logging
import logging.handlers
import sys
import signal
import argparse
import time
import client

# Deafults
LOG_FILENAME = "/tmp/entoi-client.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Configure logging to log to a file, making a new file at midnight and
# keeping the last 3 day's data
LOGGER = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
LOGGER.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and
# keeping 3 backups
HANDLER = logging.handlers.TimedRotatingFileHandler(
    LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
FORMATTER = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
HANDLER.setFormatter(FORMATTER)
# Attach the handler to the logger
LOGGER.addHandler(HANDLER)

class EnttoiLogger(object):
    """"Class to capture stdout and sterr in the log"""

    def __init__(self, logger, level):
        self.logger = logger
        self.level = level

    def write(self, message):
        """Only log if there is a message (not just a new line)"""

        if message.rstrip() != "":
            self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO and ERROR level
sys.stdout = EnttoiLogger(LOGGER, logging.INFO)
sys.stderr = EnttoiLogger(LOGGER, logging.ERROR)

# get configuration of gateway from passed arguments
PARSER = argparse.ArgumentParser(description="Enttoi service")
PARSER.add_argument("-e", "--endpoint", help="gateway API endpoint address")
PARSER.add_argument("-t", "--token", help="authorization token to gateway")
ARGS = PARSER.parse_args()

END_POINT = ""
CLIENT_TOKEN = ""
if ARGS.endpoint:
    END_POINT = ARGS.endpoint
if ARGS.token:
    CLIENT_TOKEN = ARGS.token

if not END_POINT or not CLIENT_TOKEN:
    print("Endpoint or/and client token not specified")
    sys.exit(1)

# start client and handle stop
CLN = client.Client(END_POINT, CLIENT_TOKEN)
CLN.start()


def signal_term_handler(signal, frame):
    """The method invoked by OS before killing process"""
    CLN.stop()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)

# block main thread
while True:
    time.sleep(1)
