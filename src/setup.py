"""
    Setup functions
"""
import logging
import sys

import requests


class StaticObjects:
    """Immutable objects needed for queries and data processing"""

    KEY = ""
    HEROES = {}

    @classmethod
    def setup(cls):
        """Set up all required objects"""
        cls.load_api_key()
        cls.load_hero_data()

    @classmethod
    def load_api_key(cls):
        with open("secret/steam_key.txt", "r") as ffile:
            cls.KEY = ffile.read()

    @classmethod
    def load_hero_data(cls):
        hero_data = requests.get(
            "http://api.steampowered.com/IEconDOTA2_570/GetHeroes/v1",
            params={"key": cls.KEY, "language": "en-GB"},
        ).json()
        cls.HEROES = {hero["id"]: hero["localized_name"] for hero in hero_data["result"]["heroes"]}


def setup_logger():
    """Setup the logger"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s]-[%(funcName)s]-[%(levelname)s]: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
