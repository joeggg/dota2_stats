"""
    Fetching and processing match data
"""
import asyncio
import logging
from datetime import datetime
from typing import List, Optional

from aiohttp import ClientError, ClientSession

from .setup import StaticObjects

HISTORY_ENDPOINT = "http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1"
DETAILS_ENDPOINT = "http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1"
PLAYER_ENDPOINT = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002"
DEFAULT_MATCHES_PER_PAGE = 20


async def async_request(
    url: str,
    params: Optional[dict] = None,
    method: str = "GET",
    attempts: int = 10,
) -> dict:
    """Make an async HTTP request to Steam safely"""
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


async def get_match_data(match_id: str, account_id: str) -> dict:
    data = await async_request(
        DETAILS_ENDPOINT,
        params={"match_id": match_id},
    )
    match = data.get("result")
    if not match:
        logging.info("No match in response")
        return
    # Get player info (like what team is the player on)
    player_details = extract_player_details(match["players"], account_id)
    # Get time info
    match_length = get_match_length(int(match["duration"]))
    start_time = datetime.fromtimestamp(float(match["start_time"]))
    # Format results
    return {
        "start_time": start_time.isoformat().replace("T", " "),
        "length": match_length,
        "match_id": match["match_id"],
        "result": "won" if player_details["is_radiant"] == match["radiant_win"] else "lost",
        "hero": player_details["hero"],
    }


def extract_player_details(players: List[dict], account_id: str) -> dict:
    """Return required player info from the match player list"""
    is_radiant = None
    hero = None
    for player in players:
        if player["account_id"] == int(account_id):
            is_radiant = player["player_slot"] < 5
            hero = StaticObjects.HEROES[player["hero_id"]]
            break

    return {
        "is_radiant": is_radiant,
        "hero": hero,
    }


def get_match_length(duration_s: int) -> str:
    """Get the match duration in a human readable form"""
    hours = (duration_s - duration_s % 3600) / 3600
    mins = ((duration_s - duration_s % 60) / 60) - hours * 60
    seconds = duration_s - mins * 60 - hours * 3600
    match_length = f"{int(seconds)}" if seconds > 9 else f"0{int(seconds)}"
    if mins:
        match_length = f"{int(mins)}:{match_length}"
    if hours:
        match_length = f"{int(hours)}:{match_length}"
    return match_length


async def get_player(account_id: str) -> dict:
    """Get player summary info"""
    # Generate 64 bit ID
    steamid_64 = str(int(account_id) + 76561197960265728)
    data = await async_request(
        PLAYER_ENDPOINT,
        params={"steamids": steamid_64},
    )
    try:
        player = data["response"]["players"][0]
    except (KeyError, IndexError) as exc:
        logging.error("Player info in invalid format: %s", exc)
        return

    created_at = datetime.fromtimestamp(float(player["timecreated"]))
    return {
        "name": player["personaname"],
        "avatar": player["avatarfull"],
        "created_at": created_at.isoformat().replace("T", " "),
    }


async def get_matches(account_id: str, num_matches: int = DEFAULT_MATCHES_PER_PAGE) -> List[dict]:
    data = await async_request(
        HISTORY_ENDPOINT,
        params={
            "account_id": account_id,
            "matches_requested": num_matches,
        },
    )
    if not data:
        logging.error("No match list data returned")
        return

    match_list = data.get("result", {}).get("matches")
    if not match_list:
        logging.error("Match list in invalid format")
        return

    futures = []
    for match in match_list:
        match_id = match["match_id"]
        futures.append(get_match_data(match_id, account_id))
    results = await asyncio.gather(*futures)

    return results
