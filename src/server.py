"""
    HTTP server for rendering the frontend
"""
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
        self.app.add_url_rule("/test", view_func=routes.test_html)

    def run(self) -> None:
        print("Starting server")
        self.server = create_server(self.app, listen="127.0.0.1:5656")
        self.server.run()

    def shutdown(self) -> None:
        print("Trying to shut down server")
        if self.is_alive():
            self.server.close()
        self.join(5)

        if not self.is_alive():
            print("Server has shut down")
        else:
            print("Server could not be closed")
