"""
Main entry point to application when running client from shell
"""
from __future__ import print_function
import os
import sys
import client

def main():
    """main entry point to application"""

    end_point = ""
    client_token = ""

    if "ENTTOI_ENDPOINT" in os.environ:
        end_point = os.environ["ENTTOI_ENDPOINT"]

    if "ENTTOI_CLIENT_TOKEN" in os.environ:
        client_token = os.environ["ENTTOI_CLIENT_TOKEN"]

    if not end_point or not client_token:
        print("Endpoint or/and client token not specified")
        sys.exit(1)

    clnt = client.Client(end_point, client_token)
    print("Hit 'Enter' or 'Ctr+C' to exit...\n")

    clnt.start()
    try:
        # block main thread
        input("")
    except KeyboardInterrupt:
        pass

    clnt.stop()

if __name__ == "__main__":
    main()
    sys.exit(0)
