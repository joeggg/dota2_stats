"""
    Fetching and processing match data
"""
from typing import Iterator

import requests
from requests.exceptions import HTTPError


HISTORY_ENDPOINT = "http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1"
DETAILS_ENDPOINT = "http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1"

with open("secret/steam_key.txt", "r") as ffile:
    KEY = ffile.read()


def get_match_data(match_id: str) -> dict:
    try:
        resp = requests.get(
            DETAILS_ENDPOINT,
            params={
                "key": KEY,
                "match_id": match_id,
            },
        )
        resp.raise_for_status()
    except HTTPError as exc:
        print(f"Details request failed for match {match_id}: {exc}")
        return None
    data = resp.json()
    return data["result"]


def get_matches(account_id: str, num_matches: int = 5) -> Iterator[dict]:
    try:
        resp = requests.get(
            HISTORY_ENDPOINT,
            params={
                "key": KEY,
                "account_id": account_id,
                "matches_requested": num_matches,
            },
        )
        resp.raise_for_status()
    except HTTPError as exc:
        print(exc)
        return

    data = resp.json()
    match_list = data["result"]["matches"]
    for match in match_list:
        match_id = match["match_id"]
        yield get_match_data(match_id)
