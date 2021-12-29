"""
    Fetching and processing match data
"""
import asyncio
from typing import Iterator, Optional

from aiohttp import ClientError, ClientSession


HISTORY_ENDPOINT = "http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1"
DETAILS_ENDPOINT = "http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1"

with open("secret/steam_key.txt", "r") as ffile:
    KEY = ffile.read()


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


async def get_match_data(match_id: str) -> dict:
    data = await async_request(
        DETAILS_ENDPOINT,
        params={
            "key": KEY,
            "match_id": match_id,
        },
    )
    print(f"Got match {match_id}")
    return data.get("result")


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
        futures.append(get_match_data(match_id))
    results = await asyncio.gather(*futures)

    return results
