from pydantic import BaseModel


class PlayerData(BaseModel):
    name: str
    avatar: str
    created_at: str
