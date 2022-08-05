"""
    Graceful exit
"""
import logging
import os
import signal

from src.server import ServerThread


class SigHandler:
    """
    Kill and interrupt signal handler
    """

    def __init__(self, server: ServerThread) -> None:
        self.server = server
        self.default_sigint = signal.getsignal(signal.SIGINT)
        self.default_sigterm = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGINT, self.graceful_exit)
        signal.signal(signal.SIGTERM, self.graceful_exit)

    def graceful_exit(self, signum: int, _) -> None:
        logging.info("Caught signal %s, shutting down...", signum)
        self.server.shutdown(timeout=5)
        signal.signal(signal.SIGINT, self.default_sigint)
        signal.signal(signal.SIGTERM, self.default_sigterm)
        os.kill(os.getpid(), signum)
