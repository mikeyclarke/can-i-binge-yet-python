from datetime import datetime
from typing import Any, TypedDict, List, Optional
from src.py.themoviedb import TheMovieDbClient
from src.py.url import SlugGenerator
from .ShowImageFormatter import ShowImageFormatter, ShowImage
from flag import flag


class ShowSearchResult(TypedDict):
    tmdb_id: int
    title: str
    countries_emoji: list[str]
    year: Optional[int]
    overview: Optional[str]
    poster_image: Optional[ShowImage]
    slug: str
    url_path: str


class ShowSearchResults(TypedDict):
    page: int
    shows: list[ShowSearchResult]
    total_results: int
    total_pages: int


class ShowSearch:
    def __init__(
        self,
        show_image_formatter: ShowImageFormatter,
        slug_generator: SlugGenerator,
        tmdb_client: TheMovieDbClient,
    ) -> None:
        self.__show_image_formatter = show_image_formatter
        self.__slug_generator = slug_generator
        self.__tmdb_client = tmdb_client

    def search(self, search_token: str, page: int = 1) -> ShowSearchResults:
        response_body = self.__tmdb_client.search_shows(search_token, page)
        return self.__format_results(response_body)

    def __format_results(self, response_body: dict[str, Any]) -> ShowSearchResults:
        formatted: ShowSearchResults = {
            'page': response_body['page'],
            'shows': [],
            'total_results': response_body['total_results'],
            'total_pages': response_body['total_pages'],
        }

        for result in response_body['results']:
            tmdb_id = result['id']
            slug = self.__slug_generator.generate(result['name'])

            show: ShowSearchResult = {
                'tmdb_id': tmdb_id,
                'title': result['name'],
                'countries_emoji': [flag(code) for code in result['origin_country']],
                'year': None,
                'overview': result['overview'],
                'poster_image': None,
                'slug': slug,
                'url_path': f'{tmdb_id}-{slug}',
            }

            if 'first_air_date' in result and result['first_air_date'] is not None and result['first_air_date'] != '':
                air_date = datetime.strptime(result['first_air_date'], '%Y-%m-%d')
                show['year'] = air_date.year

            if result['poster_path'] is not None:
                show['poster_image'] = self.__show_image_formatter.format('poster', result.get('poster_path'))

            formatted['shows'].append(show)

        return formatted
