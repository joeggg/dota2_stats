"""
    Fetching and processing match data with the Steam API
"""
import asyncio
import logging
from datetime import datetime
from typing import Optional

from . import consts
from .types import AccountInfo, MatchData, MatchDetails, PlayerDetails
from ..utils.setup import StaticObjects
from ..utils.tools import async_request, format_date


def get_steamid_64(account_id: str) -> str:
    """Generate 64 bit ID"""
    return str(int(account_id) + consts.STEAM64_MAX_ID)


async def get_player(account_id: str) -> AccountInfo | None:
    """Get player summary info"""
    if account_id in StaticObjects.CACHE:
        logging.debug("Found cached player summary")
        return AccountInfo(**StaticObjects.CACHE[account_id])
    # API call
    data = await async_request(
        consts.PLAYER_ENDPOINT,
        params={"steamids": get_steamid_64(account_id)},
    )
    try:
        player = data["response"]["players"][0]
    except (KeyError, IndexError) as exc:
        logging.error("Player info in invalid format: %s", exc)
        return None

    created_at = datetime.fromtimestamp(float(player["timecreated"]))
    date, _ = format_date(created_at)
    player_out = AccountInfo(
        name=player["personaname"],
        avatar=player["avatarfull"],
        created_at=date,
    )
    StaticObjects.CACHE[account_id] = player_out.dict()
    return player_out


async def get_matches(
    account_id: str,
    num_matches: int = consts.DEFAULT_MATCHES_PER_PAGE,
) -> list[MatchData] | None:
    """Get a list of the last N matches UI data concurrently"""
    # Query API for summary list
    data = await async_request(
        consts.HISTORY_ENDPOINT,
        params={
            "account_id": account_id,
            "matches_requested": num_matches,
        },
    )
    if not data:
        logging.error("No match list data returned")
        return None

    match_list = data.get("result", {}).get("matches")
    if not match_list:
        logging.error("Match list in invalid format")
        return None

    # Get match details in parallel
    futures = []
    for match in match_list:
        match_id = str(match["match_id"])
        futures.append(get_match(match_id, account_id))
    results = await asyncio.gather(*futures)

    return results


async def get_match(match_id: str, account_id: Optional[str] = None) -> MatchData | None:
    """Get a single match's data and format for the UI"""
    # Get match data from cache or API
    match: MatchDetails | None
    if match_id in StaticObjects.CACHE:
        logging.debug("Found cached match data for match %s", match_id)
        match = MatchDetails(**StaticObjects.CACHE[match_id])
    else:
        logging.debug("Querying for match %s", match_id)
        match = await fetch_match_details(match_id)
    if not match:
        return None

    # Get player summary for game from cache or match data
    player_results: PlayerDetails | None
    if account_id:
        key = f"{account_id}/{match_id}"
        if key in StaticObjects.CACHE:
            logging.debug("Found cached player results for match %s", match_id)
            player_results = PlayerDetails(**StaticObjects.CACHE[key])
        else:
            logging.debug("Generating player results for match %s", match_id)
            player_results = extract_player_results(match, account_id, key)
    else:
        player_results = None

    return MatchData(
        details=match,
        player=player_results,
    )


async def fetch_match_details(match_id: str) -> MatchDetails | None:
    """Request match data and format"""
    # API call
    data = await async_request(
        consts.DETAILS_ENDPOINT,
        params={"match_id": match_id},
    )
    match = data.get("result")
    if not match:
        logging.info("No match in response")
        return None
    # Get players info
    player_details = extract_player_details(match["players"])
    # Get time info
    match_length = extract_match_length(int(match["duration"]))
    start_time = datetime.fromtimestamp(float(match["start_time"]))
    date, time = format_date(start_time)

    # Format results
    match_out = MatchDetails(
        match_id=match_id,
        game_mode=consts.GAME_MODES[match.get("game_mode", 0)],
        start_time=f"{date} {time}",
        length=match_length,
        winner="Radiant" if match.get("radiant_win") else "Dire",
        radiant_win=match.get("radiant_win"),
        cluster=match.get("cluster"),
        players=player_details,
    )
    StaticObjects.CACHE[match_id] = match_out.dict()
    return match_out


def extract_player_details(players: list[dict]) -> list[PlayerDetails]:
    """Return required player info from the match player list"""
    results = []
    spare_id = 0
    for player in players:
        # Find team and true slot
        if player["player_slot"] < 5:
            is_radiant = True
            slot = player["player_slot"]
        else:
            is_radiant = False
            slot = player["player_slot"] - 128 + 5
        # Handle items with stored item data
        items = [StaticObjects.ITEMS[player.get(f"item_{i}", 0)] for i in range(6)]
        backpack = [StaticObjects.ITEMS[player.get(f"backpack_{i}", 0)] for i in range(3)]

        # Handle anonymous accounts
        account_id = player["account_id"]
        if account_id == consts.STEAM32_ANON_ID:
            account_id = spare_id
            spare_id += 1

        results.append(
            PlayerDetails(
                id=account_id,
                slot=slot,
                is_radiant=is_radiant,
                hero=StaticObjects.HEROES[player.get("hero_id", 0)],
                level=player.get("level"),
                kills=player.get("kills"),
                deaths=player.get("deaths"),
                assists=player.get("assists"),
                cs=player.get("last_hits"),
                denies=player.get("denies"),
                gpm=player.get("gold_per_min"),
                xpm=player.get("xp_per_min"),
                net_worth=player.get("net_worth"),
                aghs_scepter=player.get("aghanims_scepter") == 1,
                aghs_shard=player.get("aghanims_shard") == 1,
                moonshard=player.get("moonshard") == 1,
                hero_damage=player.get("hero_damage"),
                tower_damage=player.get("tower_damage"),
                healing=player.get("hero_healing"),
                items=items,
                backpack=backpack,
                neutral=StaticObjects.ITEMS[player.get("item_neutral", 0)],
            )
        )

    return results


def extract_match_length(duration_s: int) -> str:
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


def extract_player_results(match: MatchDetails, account_id: str, key: str) -> PlayerDetails | None:
    """Get result and hero for player's match list"""
    for player in match.players:
        if str(player.id) == account_id:
            player.result = "won" if player.is_radiant == match.radiant_win else "lost"
            StaticObjects.CACHE[key] = player.dict()
            return player
    return None
