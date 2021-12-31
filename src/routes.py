"""
    Handler functions for the different routes
"""
import functools
import logging
import time
from typing import List

from flask import make_response

from .dota2 import queries


def format_response(func):
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


@format_response
async def status():
    logging.info("Received status command")
    return "Hello world!"


@format_response
async def matches(account_id: str) -> List[dict]:
    """Return formatted match data to the frontend"""
    if not account_id:
        return "Invalid account ID"

    logging.info(f"Fetching match data for account {account_id}")
    matches = await queries.get_matches(account_id)
    return matches


@format_response
async def player(account_id: str) -> dict:
    """Return formatted player data to the frontend"""
    if not account_id:
        return "Invalid account ID"

    logging.info(f"Fetching player data for account {account_id}")
    player = await queries.get_player(account_id)
    return player
