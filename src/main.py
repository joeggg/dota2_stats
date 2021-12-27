"""
    App main entry point
"""
import time

from .server import ServerThread


def main():
    server = ServerThread()
    server.start()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    server.shutdown()


main()
