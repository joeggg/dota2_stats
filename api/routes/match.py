"""
    Matches routes handler functions
"""

from enum import Enum
import json
import logging

from fastapi import HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel

from ..dotaio import queries
from ..utils import get_redis


PARSER_QUEUE = "parser:work"
PARSER_RESULT = "parser:result:"


router = APIRouter(prefix="/match")


class ParseStatus(str, Enum):
    QUEUED = "queued"
    COMPLETE = "complete"
    NONE = "none"


class ParseResponse(BaseModel):
    status: ParseStatus
    message: str | None
    result: dict | None


@router.get("/{match_id}")
async def match(match_id: str, account_id: str | None = None) -> dict:
    """Return formatted match data to the frontend"""
    if not match_id or len(match_id) != 10:
        return "Invalid match ID"

    logging.info("Fetching match data for match %s", match_id)
    match_data = await queries.get_match(match_id, account_id)
    return match_data


@router.get("/{match_id}/parse", response_model=ParseResponse)
def get_parse(match_id: str):
    if len(match_id) != 10:
        raise HTTPException(status_code=400, detail="Invalid match ID")

    r = get_redis()
    result = r.get(f"{PARSER_RESULT}{match_id}")

    if result is None:
        return ParseResponse(status=ParseStatus.NONE, message="parse not found")
    if result == ParseStatus.QUEUED:
        return ParseResponse(status=ParseStatus.QUEUED, message="Replay parse in progress")

    return ParseResponse(status=ParseStatus.COMPLETE, result=json.loads(result))


@router.post("/{match_id}/parse", response_model=ParseResponse)
def post_parse(match_id: str):
    if len(match_id) != 10:
        raise HTTPException(status_code=400, detail="Invalid match ID")

    r = get_redis()
    result_key = f"{PARSER_RESULT}{match_id}"
    check = r.get(result_key)
    if check:
        return ParseResponse(status=ParseStatus.QUEUED, message="Replay parse in progress")

    # Set result key to prevent replay request spam
    r.set(result_key, ParseStatus.QUEUED, 60)
    r.lpush(PARSER_QUEUE, match_id)
    return ParseResponse(status=ParseStatus.QUEUED, message="Started replay parse")
