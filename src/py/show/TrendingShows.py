from masonite.cache import Cache
from src.py.themoviedb import TheMovieDbClient
from src.py.url import SlugGenerator
from .ShowImageFormatter import ShowImageFormatter, ShowImage
from typing import Any, Optional, TypedDict


class TrendingShowResult(TypedDict):
    tmdb_id: int
    title: str
    poster_image: Optional[ShowImage]
    slug: str
    url_path: str


class TrendingShows:
    CACHE_KEY = 'tmdb_trending_shows'
    CACHE_LIFETIME = 86400  # 1 day

    def __init__(
        self,
        cache: Cache,
        slug_generator: SlugGenerator,
        show_image_formatter: ShowImageFormatter,
        tmdb_client: TheMovieDbClient,
    ) -> None:
        self.__cache = cache
        self.__slug_generator = slug_generator
        self.__show_image_formatter = show_image_formatter
        self.__tmdb_client = tmdb_client

    def get_all(self) -> list[TrendingShowResult]:
        self.__prepare_cache()

        if self.__cache.has(self.CACHE_KEY):
            response_body = self.__cache.get(self.CACHE_KEY)
        else:
            response_body = self.__tmdb_client.get_trending_shows()
            self.__cache.put(self.CACHE_KEY, response_body, seconds=self.CACHE_LIFETIME)

        return self.__format_results(response_body)

    def __format_results(self, response_body: dict[str, Any]) -> list[TrendingShowResult]:
        formatted: list[TrendingShowResult] = []

        for result in response_body['results']:
            tmdb_id = result['id']
            slug = self.__slug_generator.generate(result['name'])

            show: TrendingShowResult = {
                'tmdb_id': tmdb_id,
                'title': result['name'],
                'poster_image': None,
                'slug': slug,
                'url_path': f'{tmdb_id}-{slug}',
            }

            if result['poster_path'] is not None:
                show['poster_image'] = self.__show_image_formatter.format('poster', result.get('poster_path'))

            formatted.append(show)

        return formatted

    def __prepare_cache(self) -> None:
        driver = self.__cache.get_driver()
        driver.set_options(self.__cache.get_config_options())
        driver.get_connection()
