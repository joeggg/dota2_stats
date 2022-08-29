from functools import wraps
import json
import logging
from secrets import token_hex
from typing import Any, Callable, List

from redis import Redis, RedisError

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_ATTEMPTS = 5


def get_redis() -> Redis:
    return Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def retry(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        for i in range(1, REDIS_ATTEMPTS + 1):
            try:
                return func(*args, **kwargs)
            except RedisError as exc:
                logging.error("Failed to cache to Redis (attempt %s): %s. Retrying", i, exc)
        raise exc

    return wrapper


class TTLCache:
    """Redis based TTL cache"""

    def __init__(self, capacity: int, ttl: int) -> None:
        self.capacity = capacity
        self.ttl = ttl
        self.__db = get_redis()
        self.prefix = token_hex(4)

    def __contains__(self, item: str) -> bool:
        return self._key(item) in self.keys()

    def __len__(self) -> int:
        return len(self.keys())

    def __getitem__(self, key: str) -> str:
        if (item := self.get(key)) is None:
            raise KeyError
        return item

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)

    def keys(self) -> List[str]:
        return self.__db.keys(self._key("*"))

    def pop(self) -> None:
        """Deletes a random item, not ideal but only used when overflowing"""
        self.__db.delete(self.keys()[0])

    def _key(self, key: str) -> str:
        """Get the full key name by adding the prefix"""
        return f"{self.prefix}:{key}"

    @retry
    def set(self, key: str, value: dict, ttl: int | None = None) -> bool:
        """Set a key to a dict value in Redis"""
        while len(self) >= self.capacity:
            self.pop()
        return self.__db.set(self._key(key), json.dumps(value), ttl or self.ttl)

    @retry
    def get(self, key: str, default: dict | None = None) -> dict | None:
        """
        Get the dict stored at the given key in Redis. Returns the default if it doesn't exist
        """
        if (value := self.__db.get(self._key(key))) is None:
            return default
        return json.loads(value)
