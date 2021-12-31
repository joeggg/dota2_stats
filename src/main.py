"""
    App main entry point
"""
import time

from .server import ServerThread
from .setup import setup_logger, StaticObjects


def main():
    StaticObjects.setup()
    setup_logger()
    server = ServerThread()
    server.start()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    server.shutdown()


main()
