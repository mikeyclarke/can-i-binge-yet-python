from masonite.cache import Cache as MasoniteCache
from typing import Any


class Cache:
    def __init__(self, base_cache: MasoniteCache) -> None:
        self.__base_cache = base_cache
        self.__cache_prepped = False

    def has(self, key: str) -> bool:
        self.__prepare_cache()
        return self.__base_cache.has(key)

    def get(self, key: str) -> Any:
        self.__prepare_cache()
        return self.__base_cache.get(key)

    def put(self, key: str, value: Any, seconds: int) -> None:
        self.__base_cache.put(key, value, seconds)

    def __prepare_cache(self) -> None:
        if self.__cache_prepped:
            return

        driver = self.__base_cache.get_driver()
        driver.set_options(self.__base_cache.get_config_options())
        driver.get_connection()

        self.__cache_prepped = True
