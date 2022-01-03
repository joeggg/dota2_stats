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
from flask import make_response

from .setup import StaticObjects


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
            logging.debug(exc.headers)
            logging.error(f"{exc}: Attempt {attempt+1} of {attempts}")
            await asyncio.sleep(0.2)
            continue

    return {}


def format_server_response(func):
    """Adds required headers to response and times the function"""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        data = await func(*args, **kwargs)
        end = time.perf_counter()
        logging.info("Time taken for %s: %ss", func.__name__, end - start)

        data = {"results": data}
        resp = make_response(data)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        logging.info(resp)

        return resp

    return wrapper


def format_date(datetime: datetime) -> Tuple[str, str]:
    """Returns formatted date and time separately"""
    date, time = datetime.isoformat().split("T")
    year, month, day = date.split("-")
    return f"{day}/{month}/{year}", time
