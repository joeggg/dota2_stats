"""
    Interface to the Dota 2 game coordinator for downloading replays
"""
import logging
import threading

import requests
from steam.client import SteamClient
from dota2.client import Dota2Client
from dota2.protobufs.dota_gcmessages_common_pb2 import CMsgDOTAMatch

from ..utils.setup import StaticObjects


class Dota2Thread(threading.Thread):
    """Thread for running dota 2 queries"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.client: SteamClient
        self.dota: Dota2Client
        self.name = "Dota2ClientThread"

    def run(self):
        """Connect to dota 2 coordinator and wait for commands"""
        self.client = SteamClient()
        self.client.on("logged_on", callback=self.start_dota)
        self.client.on("auth_code_required", callback=self.auth_code_prompt)

        self.dota = Dota2Client(self.client)
        self.dota.on("match_details", callback=self.process_match_data)

        logging.info("Starting steam CLI")
        try:
            self.client.login(**StaticObjects.CREDENTIALS.get())
        except Exception as exc:
            logging.info(exc)
            logging.exception(exc)
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
        logging.info("Shutting down Dota2ClientThread")
        self.client.logout()
        self.dota.exit()

    def start_dota(self):
        self.dota.launch()
        logging.info("Dota 2 client launched")

    def get_match_data(self, match_id):
        self.dota.request_match_details(match_id)

    def process_match_data(self, match_id, eresult, data: CMsgDOTAMatch):
        dl_url = f"http://replay{data.cluster}.valve.net/570/{match_id}_{data.replay_salt}.dem.bz2"
        download_file(dl_url, dl_url.split("/")[-1])

    def process_data(self, *args):
        print(args)


def download_file(url: str, filename: str) -> None:
    logging.info("Downloading from %s", url)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    logging.info("Finished downloading")
