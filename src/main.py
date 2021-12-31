"""
    App main entry point
"""
import time

from .dota2.thread import Dota2Thread
from .server import ServerThread
from .utils.setup import setup_logger, StaticObjects


def main():
    StaticObjects.setup()
    setup_logger()
    server = ServerThread()
    dota2 = Dota2Thread()
    dota2.start()
    # server.start()

    # while True:
    #     try:
    #         time.sleep(0.1)
    #     except KeyboardInterrupt:
    #         break

    # server.shutdown()


main()
