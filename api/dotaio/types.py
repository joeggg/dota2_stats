from pydantic import BaseModel


class AccountInfo(BaseModel):
    name: str
    avatar: str
    created_at: str


class PlayerDetails(BaseModel):
    id: int
    result: str | None
    slot: int
    is_radiant: bool
    hero: str
    level: int | None
    kills: int | None
    deaths: int | None
    assists: int | None
    cs: int | None
    denies: int | None
    gpm: int | None
    xpm: int | None
    net_worth: int | None
    hero_damage: int | None
    tower_damage: int | None
    healing: int | None
    aghs_scepter: bool
    aghs_shard: bool
    moonshard: bool
    items: list[dict[str, str] | None]
    backpack = list[dict[str, str] | None]
    neutral: dict[str, str] | None


class MatchDetails(BaseModel):
    match_id: str
    game_mode: str
    start_time: str
    length: str
    winner: str
    radiant_win: bool | None
    cluster: int | None
    players: list[PlayerDetails]


class MatchData(BaseModel):
    details: MatchDetails
    player: PlayerDetails | None
