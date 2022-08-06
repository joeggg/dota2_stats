"""
    Constants useful in the Dota2 module that do not need configuration
"""

HISTORY_ENDPOINT = "http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1"
DETAILS_ENDPOINT = "http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1"
PLAYER_ENDPOINT = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002"
DEFAULT_MATCHES_PER_PAGE = 20
STEAM64_MAX_ID = 76561197960265728
STEAM32_ANON_ID = 4294967295

GAME_MODES = {
    0: None,
    1: "All Pick",
    2: "Captain's Mode",
    3: "Random Draft",
    4: "Single Draft",
    5: "All Random",
    6: "Intro",
    7: "Diretide",
    8: "Reverse Captain's Mode",
    9: "The Greeviling",
    10: "Tutorial",
    11: "Mid Only",
    12: "Least Played",
    13: "New Player Pool",
    14: "Compendium Matchmaking",
    15: "Co-op vs Bots",
    16: "Captains Draft",
    18: "Ability Draft",
    20: "All Random Deathmatch",
    21: "1v1 Mid Only",
    # 22: "Ranked Matchmaking",
    22: "All Pick",  # all pick game modes returning 22 for some reason
    23: "Turbo Mode",
}
