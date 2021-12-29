"""
    Handler functions for the different routes
"""
import functools
import time

from flask import make_response

from . import queries


def format_response(func):
    """Adds required headers to response"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        data = {"results": data}
        resp = make_response(data)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        print(resp)
        return resp

    return wrapper


@format_response
def status():
    print("Received status command")
    return "Hello world!"


@format_response
def matches(account_id: str) -> str:
    """Return formatted match data to the browser"""
    if not account_id:
        return "Invalid account ID"

    print(f"Fetching match data for account {account_id}")
    start = time.perf_counter()
    matches = queries.get_matches(account_id)
    output = []
    for match in matches:
        print(f'Got match {match["match_id"]}')
        output.append(match)
    print(f"Time taken: {time.perf_counter() - start}s")

    return output
