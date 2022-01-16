"""
    Interface to the Dota 2 game coordinator for downloading replays
"""
import logging
import threading

from steam.client import SteamClient
from dota2.client import Dota2Client

from ..utils.setup import StaticObjects


class Dota2Thread(threading.Thread):
    """Thread for running dota 2 queries"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.client = SteamClient()
        self.dota = Dota2Client(self.client)
        self.name = "Dota2ClientThread"
        self.client.on("logged_on", callback=self.start_dota)
        self.client.on("auth_code_required", callback=self.auth_code_prompt)
        self.dota.on("match_details", callback=self.process_match_data)

    def run(self):
        logging.info("Starting steam CLI")
        try:
            self.client.login(**StaticObjects.CREDENTIALS.get())
        except Exception as exc:
            logging.info(exc)
            logging.exception(exc)
        # self.client.cli_login()
        logging.info("Logged into CLI")
        self.client.run_forever()

    def auth_code_prompt(self, is_2fa, code_mismatch):
        if is_2fa:
            code = input("Enter 2FA Code: ")
            self.client.login(**StaticObjects.CREDENTIALS.get(), two_factor_code=code)
        else:
            code = input("Enter Email Code: ")
            self.client.login(**StaticObjects.CREDENTIALS.get(), auth_code=code)

    def shutdown(self):
        self.dota.exit()
        self.client.disconnect()

    def start_dota(self):
        self.dota.launch()
        logging.info("Dota 2 client launched")
        self.get_match_data()

    def get_match_data(self):
        self.dota.request_match_details(6347209718)

    def process_match_data(self, *args):
        logging.info("hi")
        logging.info(args)

    def process_data(self, *args):
        print(args)
