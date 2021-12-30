"""
    App main entry point
"""
import time

from .server import ServerThread
from .setup import StaticObjects


def main():
    StaticObjects.setup()
    server = ServerThread()
    server.start()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    server.shutdown()


main()
