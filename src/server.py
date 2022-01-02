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
    def __init__(self, *args, **kwargs):
        self.app = Flask("dota2_stats")
        self.server: BaseWSGIServer
        super().__init__(*args, **kwargs)
        self.app.add_url_rule("/status", view_func=routes.status)
        self.app.add_url_rule("/matches/<account_id>", view_func=routes.matches)
        self.app.add_url_rule("/player/<account_id>", view_func=routes.player)
        self.app.add_url_rule("/match/<match_id>", view_func=routes.match)

    def run(self) -> None:
        logging.info("Starting server")
        self.server = create_server(self.app, listen="0.0.0.0:5656")
        self.server.run()

    def shutdown(self) -> None:
        logging.info("Trying to shut down server")
        if self.is_alive():
            self.server.close()
        self.join(20)

        if not self.is_alive():
            logging.info("Server has shut down")
        else:
            logging.info("Server could not be closed")
