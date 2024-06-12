from typing import Any


class LocalCache:
    local_cache = {}

    @staticmethod
    def set_value(key: str, value: Any) -> str:
        LocalCache.local_cache[key] = value
        return value

    @staticmethod
    def get_value(key: str) -> Any:
        return LocalCache.local_cache.get(key)

    @staticmethod
    def remove_value(key: str) -> str:
        return LocalCache.local_cache.pop(key, None)
