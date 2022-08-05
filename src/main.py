"""
    App main entry point
"""

import logging
import time

from .server import ServerThread
from .utils.setup import setup_logger, StaticObjects
from .utils.sighandler import SigHandler


def main():
    """Start all threads needed"""
    setup_logger()
    StaticObjects.setup()
    server = ServerThread()
    _ = SigHandler(server)
    server.start()

    start = time.time()
    heartbeat_interval = 600
    while True:
        time.sleep(1)
        now = time.time()
        if now - start > heartbeat_interval:
            logging.info("Heartbeat \u2665")
            start = now


main()
