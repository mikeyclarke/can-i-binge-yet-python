from masonite.cache import Cache
from .TheMovieDbClient import TheMovieDbClient
from typing import Any, Optional, cast


class TheMovieDbConfiguration:
    CACHE_KEY = 'tmdb_configuration'
    CACHE_LIFETIME = 86400 * 5  # 5 days

    __configuration: Optional[dict[str, Any]]

    def __init__(self, cache: Cache, tmdb_client: TheMovieDbClient) -> None:
        self.__cache = cache
        self.__tmdb_client = tmdb_client
        self.__configuration = None

    def get_image_base_url(self) -> str:
        configuration = self.__get_configuration()

        result = configuration['images']['secure_base_url']
        if not isinstance(result, str):
            raise TypeError()

        return result

    def get_image_sizes(self, image_type: str) -> list[str]:
        configuration = self.__get_configuration()
        images_configuration = configuration.get('images')
        key = f'{image_type}_sizes'

        if not isinstance(images_configuration, dict):
            raise TypeError()

        if key not in images_configuration:
            raise KeyError

        result = images_configuration.get(key)
        result = cast(list[str], result)
        return result

    def __get_configuration(self) -> dict[str, Any]:
        if self.__configuration is not None:
            return self.__configuration

        self.__prepare_cache()

        if self.__cache.has(self.CACHE_KEY):
            configuration = self.__cache.get(self.CACHE_KEY)
        else:
            configuration = self.__fetch_configuration()
            self.__cache.put(self.CACHE_KEY, configuration, seconds=self.CACHE_LIFETIME)

        self.__configuration = configuration
        return self.__configuration

    def __fetch_configuration(self) -> dict[str, Any]:
        return self.__tmdb_client.get_configuration()

    def __prepare_cache(self) -> None:
        driver = self.__cache.get_driver()
        driver.set_options(self.__cache.get_config_options())
        driver.get_connection()
