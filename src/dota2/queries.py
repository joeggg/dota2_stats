"""
    Fetching and processing match data
"""
import asyncio
import logging
from datetime import datetime
from typing import List, Optional

from aiohttp import ClientError, ClientSession

from ..utils.setup import StaticObjects

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


async def get_match_data(match_id: str, account_id: Optional[str] = None) -> dict:
    """
    Call API for match data and format for the UI
    """
    if match_id in StaticObjects.CACHE:
        logging.debug("Found cached match")
        return StaticObjects.CACHE[match_id]

    logging.debug("Querying for match")
    data = await async_request(
        DETAILS_ENDPOINT,
        params={"match_id": match_id},
    )
    match = data.get("result")
    if not match:
        logging.info("No match in response")
        return
    # Get players info
    player_details = extract_player_details(match["players"])
    # Get time info
    match_length = get_match_length(int(match["duration"]))
    start_time = datetime.fromtimestamp(float(match["start_time"]))
    # Get result and hero
    if account_id:
        result = (
            "won" if player_details[account_id]["is_radiant"] == match["radiant_win"] else "lost"
        )
        hero = player_details[account_id]["hero"]
    else:
        result = None
        hero = None
    # Format results
    match_out = {
        "start_time": start_time.isoformat().replace("T", " "),
        "length": match_length,
        "match_id": match_id,
        "result": result,
        "hero": hero,
        "cluster": match.get("cluster"),
        "players": player_details,
    }
    StaticObjects.CACHE[match_id] = match_out
    return match_out


def extract_player_details(players: List[dict]) -> dict:
    """Return required player info from the match player list"""
    results = {}
    spare_id = 0
    for player in players:
        if player["player_slot"] < 5:
            is_radiant = True
            slot = player["player_slot"]
        else:
            is_radiant = False
            slot = player["player_slot"] - 128 + 5

        items = [StaticObjects.ITEMS[player.get(f"item_{i}", 0)] for i in range(6)]
        backpack = [StaticObjects.ITEMS[player.get(f"backpack_{i}", 0)] for i in range(3)]

        # Handle anonymous accounts
        account_id = player["account_id"]
        if account_id == 4294967295:  # anonymous ID
            account_id = spare_id
            spare_id += 1

        results[str(account_id)] = {
            "slot": slot,
            "is_radiant": is_radiant,
            "hero": StaticObjects.HEROES[player.get("hero_id", 0)],
            "level": player.get("level"),
            "kills": player.get("kills"),
            "deaths": player.get("deaths"),
            "assists": player.get("assists"),
            "cs": player.get("last_hits"),
            "denies": player.get("denies"),
            "gpm": player.get("gold_per_min"),
            "xpm": player.get("xp_per_min"),
            "net_worth": player.get("net_worth"),
            "aghs_scepter": player.get("aghanims_scepter") == 1,
            "aghs_shard": player.get("aghanims_shard") == 1,
            "moonshard": player.get("moonshard") == 1,
            "hero_damage": player.get("hero_damage"),
            "tower_damage": player.get("tower_damage"),
            "healing": player.get("hero_healing"),
            "items": items,
            "backpack": backpack,
            "neutral": StaticObjects.ITEMS[player.get("item_neutral", 0)],
        }

    return results


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
        match_id = str(match["match_id"])
        futures.append(get_match_data(match_id, account_id))
    results = await asyncio.gather(*futures)

    return results
