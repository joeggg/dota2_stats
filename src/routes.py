"""
    Handler functions for the different routes
"""
import functools
import logging
import time

from flask import make_response

from . import queries


def format_response(func):
    """Adds required headers to response"""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        data = await func(*args, **kwargs)
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
async def matches(account_id: str) -> str:
    """Return formatted match data to the browser"""
    if not account_id:
        return "Invalid account ID"

    logging.info(f"Fetching match data for account {account_id}")
    start = time.perf_counter()
    matches = await queries.get_matches(account_id)
    logging.info(f"Time taken: {time.perf_counter() - start}s")
    return matches
