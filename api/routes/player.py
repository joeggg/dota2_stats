"""
    Player routes handler functions
"""

import logging
from typing import List

from fastapi import HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel

from ..dotaio import queries


PARSER_QUEUE = "parser:work"
PARSER_RESULT = "parser:result:"


router = APIRouter(prefix="/player")


@router.get("/{account_id}")
async def player(account_id: str) -> dict:
    """Return formatted player data to the frontend"""
    logging.info("Fetching player data for account %s", account_id)
    player_data = await queries.get_player(account_id)
    return player_data


@router.get("/{account_id}/matches")
async def matches(account_id: str) -> List[dict]:
    """Return formatted list of match data to the frontend"""
    if not account_id:
        return "Invalid account ID"

    logging.info("Fetching match data for account %s", account_id)
    matches_data = await queries.get_matches(account_id)
    return matches_data
