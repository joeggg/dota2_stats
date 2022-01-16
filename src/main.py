"""
    App main entry point
"""

import gevent.monkey

gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()
import logging
import sys
import time

from .dota2 import Dota2Thread
from .server import ServerThread
from .utils.setup import setup_logger, StaticObjects
from .utils.sighandler import SigHandler


def main():
    """Start all threads needed"""
    setup_logger()
    StaticObjects.setup()
    server = ServerThread()
    dota2 = Dota2Thread()
    _ = SigHandler(server, dota2)
    # dota2.start()
    server.start()

    start = time.time()
    heartbeat_interval = 10
    while True:
        time.sleep(1)
        now = time.time()
        if now - start > heartbeat_interval:
            logging.info("Heartbeat \u2665")
            start = now


main()
