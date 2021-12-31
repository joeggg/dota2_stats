"""
    Interface to the Dota 2 game coordinator
"""
import threading

from steam.client import SteamClient
from dota2.client import Dota2Client

from ..utils.setup import StaticObjects


class Dota2Thread(threading.Thread):
    """Thread for running dota 2 queries"""

    def __init__(self, *args, **kwargs) -> None:
        self.client: SteamClient
        self.dota: Dota2Client
        super().__init__(*args, **kwargs)

    def run(self):
        self.client = SteamClient()
        self.dota = Dota2Client(self.client)
        print(f"{StaticObjects.CREDENTIALS.get()}")
        self.client.cli_login(**StaticObjects.CREDENTIALS.get())
        print("hi")
        self.client.run_forever()

    def shutdown(self):
        self.dota.exit()
        self.client.disconnect()

    def start_dota(self):
        self.dota.launch()

    def get_match_data(self):
        self.dota.request_match_details(6347209718)

    def process_data(self, *args):
        print(args)
