"""
    App main entry point
"""
import logging
import sys
import time

from .dota2 import Dota2Thread
from .server import ServerThread
from .utils.setup import setup_logger, StaticObjects


def main():
    """Start all threads needed"""
    setup_logger()
    StaticObjects.setup()
    server = ServerThread()
    # dota2 = Dota2Thread()
    # dota2.start()
    server.start()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    server.shutdown()
    logging.info("Finised shutting down")
    sys.exit()


main()
