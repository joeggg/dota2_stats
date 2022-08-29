"""
    Setup functions
"""
import logging
import sys
import time
from typing import Awaitable, Callable, Optional

from requests import HTTPError, request
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from .cache import TTLCache


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def time_request(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
    start = time.perf_counter()
    response = await call_next(request)
    time_taken = str(time.perf_counter() - start)
    logging.info("%ss taken for request: %s", time_taken, request.url.path)
    response.headers["X-Process-Time"] = time_taken
    return response


class StaticObjects:
    """Immutable objects needed for queries and data processing"""

    CACHE = TTLCache(1000, 300)
    HEROES = {}
    ITEMS = {}
    KEY = ""

    @classmethod
    def setup(cls) -> None:
        """Set up all required objects"""
        cls.load_api_key()
        cls.load_hero_data()
        cls.load_item_data()

    @classmethod
    def load_api_key(cls) -> None:
        with open("secret/steam_key.txt", "r") as ffile:
            cls.KEY = ffile.read().strip()

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
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "[%(asctime)s]-[%(threadName)s]-[%(funcName)s]-[%(levelname)s]: %(message)s"
    )
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
            logging.exception(exc)
            logging.error(f"{exc}: Attempt {attempt+1} of {attempts}")
            time.sleep(0.2)
            continue

    return {}
