"""
    Handler functions for the different routes
"""
import json
import time

from flask import render_template

from . import queries


def status():
    return "Hello world!"


def test_html():
    return render_template("index.html")


def matches(account_id: str) -> str:
    """Return formatted match data to the browser"""
    if not account_id:
        return "Invalid account ID"

    print(f"Fetching match data for account {account_id}")
    start = time.perf_counter()
    matches = queries.get_matches(account_id)
    output = ""
    for match in matches:
        print(f'Got match {match["match_id"]}')
        output += json.dumps(match, indent=2) + "\n"
    print(f"Time taken: {time.perf_counter() - start}s")

    return output
