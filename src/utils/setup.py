"""
    Setup functions
"""
import logging
import sys
import time
from typing import Dict, List, Optional

from requests import HTTPError, request
from cachetools import TTLCache


class Credentials:
    """Store steam credentials"""

    def __init__(self) -> None:
        self.username = ""
        self.password = ""

    def set(self, credentials: List[str]) -> None:
        if len(credentials) != 2:
            raise Exception("Incorrect number of credential terms, should be username and password")
        self.username, self.password = credentials

    def get(self) -> Dict[str, str]:
        return {
            "username": self.username,
            "password": self.password,
        }


class StaticObjects:
    """Immutable objects needed for queries and data processing"""

    CACHE = TTLCache(1000, 300)
    CREDENTIALS = Credentials()
    HEROES = {}
    ITEMS = {}
    KEY = ""

    @classmethod
    def setup(cls) -> None:
        """Set up all required objects"""
        cls.load_api_key()
        # cls.load_credentials()
        cls.load_hero_data()
        cls.load_item_data()

    @classmethod
    def load_api_key(cls) -> None:
        with open("secret/steam_key.txt", "r") as ffile:
            cls.KEY = ffile.read()

    @classmethod
    def load_credentials(cls) -> None:
        with open("secret/steam_credentials.txt", "r") as ffile:
            cls.CREDENTIALS.set(ffile.read().split("\n"))

    @classmethod
    def load_hero_data(cls) -> None:
        hero_data = sync_request(
            "http://api.steampowered.com/IEconDOTA2_570/GetHeroes/v1",
            params={"key": cls.KEY, "language": "en-GB"},
        )
        cls.HEROES = {hero["id"]: hero["localized_name"] for hero in hero_data["result"]["heroes"]}
        cls.HEROES[0] = None
        logging.info("Got heroes data")

    @classmethod
    def load_item_data(cls) -> None:
        item_data = sync_request(
            "http://api.steampowered.com/IEconDOTA2_570/GetGameItems/v1",
            params={"key": cls.KEY, "language": "en-GB"},
        )
        cls.ITEMS = {
            item["id"]: {
                "name": item["localized_name"],
                "cost": item["cost"],
            }
            for item in item_data["result"]["items"]
        }
        cls.ITEMS[0] = None
        logging.info("Got items data")


def setup_logger() -> None:
    """Setup the logger"""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s]-[%(funcName)s]-[%(levelname)s]: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def sync_request(
    url: str,
    params: Optional[dict] = None,
    method: str = "GET",
    attempts: int = 10,
) -> dict:
    """Make an async HTTP request to the Steam API safely"""
    params = params or {}
    for attempt in range(attempts):
        try:
            resp = request(method, url, params=params)
            resp.raise_for_status()
            data = resp.json()
            return data
        except HTTPError as exc:
            logging.debug(exc.headers)
            logging.error(f"{exc}: Attempt {attempt+1} of {attempts}")
            time.sleep(0.2)
            continue

    return {}
