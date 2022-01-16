"""
    HTTP server for sending data to frontend
"""
import logging
import threading

from flask import Flask
from waitress import create_server
from waitress.server import BaseWSGIServer

from . import routes


class ServerThread(threading.Thread):
    """
    HTTP server thread
    """

    def __init__(self, *args, **kwargs):
        self.app = Flask("dota2_stats")
        self.server: BaseWSGIServer
        super().__init__(*args, **kwargs)
        self.name = "ServerThread"
        # Route definitions
        self.app.add_url_rule("/status", view_func=routes.status)
        self.app.add_url_rule("/matches/<account_id>", view_func=routes.matches)
        self.app.add_url_rule("/player/<account_id>", view_func=routes.player)
        self.app.add_url_rule("/match/<match_id>", view_func=routes.match)

    def run(self) -> None:
        """Starts the server thread"""
        logging.info("Starting server")
        self.server = create_server(self.app, listen="0.0.0.0:5656")
        self.server.run()

    def shutdown(self, timeout: int = 20) -> None:
        """Attempts to stop the server thread and waits for it to join"""
        logging.info("Trying to shut down server")
        if self.is_alive():
            self.server.close()
        self.join(timeout)

        if not self.is_alive():
            logging.info("Server has shut down")
        else:
            logging.info("Server could not be closed gracefully")
