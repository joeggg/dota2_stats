"""
    Player routes handler functions
"""

import logging

from fastapi import APIRouter, HTTPException

from ..dotaio import queries
from ..dotaio.types import AccountInfo, MatchData


PARSER_QUEUE = "parser:work"
PARSER_RESULT = "parser:result:"

router = APIRouter(prefix="/player")


@router.get("/{account_id}")
async def player(account_id: str) -> AccountInfo:
    """Return formatted player data to the frontend"""
    logging.info("Fetching player data for account %s", account_id)
    account = await queries.get_account(account_id)
    if not account:
        raise HTTPException(404, "Account info not found")
    return account


@router.get("/{account_id}/matches")
async def matches(account_id: str) -> list[MatchData]:
    """Return formatted list of match data to the frontend"""
    logging.info("Fetching match data for account %s", account_id)
    matches_data = await queries.get_matches(account_id)
    if matches_data is None:
        raise HTTPException(404, "No match data found")
    return matches_data
