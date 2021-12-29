"""
    Fetching and processing match data
"""
import asyncio
from datetime import datetime
from typing import Iterator, Optional

import requests
from aiohttp import ClientError, ClientSession


HISTORY_ENDPOINT = "http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1"
DETAILS_ENDPOINT = "http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1"

with open("secret/steam_key.txt", "r") as ffile:
    KEY = ffile.read()

hero_data = requests.get(
    "http://api.steampowered.com/IEconDOTA2_570/GetHeroes/v1", params={"key": KEY}
).json()
HEROES = {
    hero["id"]: hero["name"].removeprefix("npc_dota_hero_")
    for hero in hero_data["result"]["heroes"]
}


async def async_request(
    url: str,
    params: Optional[dict] = None,
    method: str = "GET",
) -> dict:
    """Make an async HTTP request safely"""
    params = params or {}
    try:
        async with ClientSession() as session:
            async with session.request(method, url, params=params) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data
    except ClientError as exc:
        print(exc)
        return {}


async def get_match_data(match_id: str, account_id: str) -> dict:
    data = await async_request(
        DETAILS_ENDPOINT,
        params={
            "key": KEY,
            "match_id": match_id,
        },
    )
    match = data.get("result")
    if not match:
        print("No match in response")
        return
    # What team is the player on
    is_radiant = None
    hero = None
    for player in match["players"]:
        if player["account_id"] == int(account_id):
            is_radiant = player["player_slot"] < 5
            hero = HEROES[player["hero_id"]]
            break
    # Format results
    start_time = datetime.fromtimestamp(float(match["start_time"]))
    return {
        "start_time": start_time.isoformat().replace("T", " "),
        "match_id": match["match_id"],
        "result": "won" if is_radiant == match["radiant_win"] else "lost",
        "hero": hero,
    }


async def get_matches(account_id: str, num_matches: int = 5) -> Iterator[dict]:
    data = await async_request(
        HISTORY_ENDPOINT,
        params={
            "key": KEY,
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
