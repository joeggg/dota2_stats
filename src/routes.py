"""
    Handler functions for the different routes
"""
import logging
from typing import List

from flask import request

from .dotaio import queries
from .utils.tools import format_server_response, get_redis


PARSER_QUEUE = "parser:work"
PARSER_RESULT = "parser:result:"


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
    player_data = await queries.get_player(account_id)
    return player_data


@format_server_response
async def matches(account_id: str) -> List[dict]:
    """Return formatted list of match data to the frontend"""
    if not account_id:
        return "Invalid account ID"

    logging.info("Fetching match data for account %s", account_id)
    matches_data = await queries.get_matches(account_id)
    return matches_data


@format_server_response
async def match(match_id: str) -> dict:
    """Return formatted match data to the frontend"""
    if not match_id or len(match_id) != 10:
        return "Invalid match ID"
    account_id = request.args.get("id")

    logging.info("Fetching match data for match %s", match_id)
    match_data = await queries.get_match(match_id, account_id)
    return match_data


@format_server_response
async def parse() -> dict:
    match_id = request.args.get("match_id")
    if not match_id or len(match_id) != 10:
        return "Invalid match ID"

    r = get_redis()
    result_key = f"{PARSER_RESULT}{match_id}"
    check = r.get(result_key)
    if check:
        return {"status": "queued", "message": "Replay parse already started"}

    # Set result key to prevent replay request spam
    r.set(result_key, "in_progress", 60)
    r.lpush(PARSER_QUEUE, match_id)
    return {"status": "queued", "message": "Replay parse started"}


@format_server_response
async def result() -> dict:
    match_id = request.args.get("match_id")
    if not match_id or len(match_id) != 10:
        return "Invalid match ID"

    r = get_redis()
    result = r.get(f"{PARSER_RESULT}{match_id}")
    if result is None:
        return {"status": "queued"}
    return {"status": "complete", "result": result}
