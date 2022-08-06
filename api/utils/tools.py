"""
    Useful tools
"""
import asyncio
import functools
import logging
import time
from datetime import datetime
from typing import Optional, Tuple

from aiohttp import ClientError, ClientSession
from redis import Redis

from .setup import StaticObjects

REDIS_HOST = "redis"
REDIS_PORT = 6379


def get_redis() -> Redis:
    return Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


async def async_request(
    url: str,
    params: Optional[dict] = None,
    method: str = "GET",
    attempts: int = 10,
) -> dict:
    """Make an async HTTP request to the Steam API safely"""
    params = params or {}
    for attempt in range(attempts):
        try:
            async with ClientSession() as session:
                async with session.request(
                    method,
                    url,
                    params={"key": StaticObjects.KEY, **params},
                ) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    return data
        except ClientError as exc:
            logging.debug(exc.args)
            logging.error(f"{exc}: Attempt {attempt+1} of {attempts}")
            await asyncio.sleep(0.1)
            continue

    return {}


def format_date(datetime: datetime) -> Tuple[str, str]:
    """Returns formatted date and time separately"""
    date, time = datetime.isoformat().split("T")
    year, month, day = date.split("-")
    return f"{day}/{month}/{year}", time
