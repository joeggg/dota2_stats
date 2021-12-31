"""
    Fetching and processing match data
"""
import asyncio
from datetime import datetime
from typing import Iterator, List, Optional

from aiohttp import ClientError, ClientSession

from .setup import StaticObjects

HISTORY_ENDPOINT = "http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1"
DETAILS_ENDPOINT = "http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1"
DEFAULT_MATCHES_PER_PAGE = 20


async def async_request(
    url: str,
    params: Optional[dict] = None,
    method: str = "GET",
    attempts: int = 10,
) -> dict:
    """Make an async HTTP request safely"""
    params = params or {}
    for attempt in range(attempts):
        try:
            async with ClientSession() as session:
                async with session.request(method, url, params=params) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    return data
        except ClientError as exc:
            print(f"{exc}: Attempt {attempt+1} of {attempts}")
            await asyncio.sleep(0.2)
            continue

    return {}


async def get_match_data(match_id: str, account_id: str) -> dict:
    data = await async_request(
        DETAILS_ENDPOINT,
        params={
            "key": StaticObjects.KEY,
            "match_id": match_id,
        },
    )
    match = data.get("result")
    if not match:
        print("No match in response")
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


async def get_matches(
    account_id: str,
    num_matches: int = DEFAULT_MATCHES_PER_PAGE,
) -> Iterator[dict]:
    data = await async_request(
        HISTORY_ENDPOINT,
        params={
            "key": StaticObjects.KEY,
            "account_id": account_id,
            "matches_requested": num_matches,
        },
    )
    if not data:
        print("No data returned")
        return
    match_list = data.get("result", {}).get("matches")
    if not match_list:
        print("Match list in invalid format")
        return

    futures = []
    for match in match_list:
        match_id = match["match_id"]
        futures.append(get_match_data(match_id, account_id))
    results = await asyncio.gather(*futures)

    return results
