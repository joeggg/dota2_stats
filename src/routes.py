"""
    Handler functions for the different routes
"""
import logging
from typing import List

from flask import request

from .dota2 import queries
from .utils.tools import format_server_response


@format_server_response
async def status():
    """Test command"""
    logging.info("Received status command")
    return "Hello world!"


@format_server_response
async def player(account_id: str) -> dict:
    """Return formatted player data to the frontend"""
    if not account_id:
        return "Invalid account ID"

    logging.info("Fetching player data for account %s", account_id)
    player = await queries.get_player(account_id)
    return player


@format_server_response
async def matches(account_id: str) -> List[dict]:
    """Return formatted list of match data to the frontend"""
    if not account_id:
        return "Invalid account ID"

    logging.info(f"Fetching match data for account {account_id}")
    matches = await queries.get_matches(account_id)
    return matches


@format_server_response
async def match(match_id: str) -> dict:
    """Return formatted match data to the frontend"""
    if not match_id:
        return "Invalid match ID"
    account_id = request.args.get("id")

    logging.info("Fetching match data for match %s", match_id)
    match = await queries.get_match(match_id, account_id)
    return match
