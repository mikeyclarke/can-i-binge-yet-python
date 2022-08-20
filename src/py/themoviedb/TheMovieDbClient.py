from masonite.configuration.Configuration import Configuration
from requests import Session
from typing import Any, Optional


default_request_options = {
    'timeout': 15,
}


class TheMovieDbClient:
    def __init__(self, config: Configuration) -> None:
        self.__config = config

    def get_configuration(self) -> dict[str, Any]:
        return self.__make_request('/3/configuration')

    def search_shows(self, search_token: str, page: int = 1) -> dict[str, Any]:
        return self.__make_request('/3/search/tv', {'query': search_token})

    def get_show(self, tmdb_show_id: int) -> dict[str, Any]:
        session = Session()

        show_details = self.__make_request(f'/3/tv/{tmdb_show_id}', {}, session)

        last_season = None
        if len(show_details['seasons']) > 0:
            last_season_number = show_details['seasons'][-1]['season_number']
            last_season = self.__make_request(
                f'/3/tv/{tmdb_show_id}/season/{last_season_number}',
                {},
                session
            )

        show_details['last_season'] = last_season
        return show_details

    def get_trending_shows(self, time_window: str = 'day') -> dict[str, Any]:
        return self.__make_request(f'/3/trending/tv/{time_window}')

    def __make_request(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        session: Optional[Session] = None,
    ) -> dict[str, Any]:
        if params is None:
            params = {}

        if session is None:
            session = Session()

        base_url = self.__config.get('application.tmdb_api_base_url')
        api_key = self.__config.get('application.tmdb_api_key')

        request_params = {
            **params,
            'api_key': api_key,
        }

        request_args = {
            'params': request_params,
            **default_request_options,  # type: ignore # see https://github.com/python/mypy/issues/10171
        }

        response = session.get(
            f'{base_url}{endpoint}',
            **request_args  # type: ignore # see https://github.com/python/mypy/issues/10171
        )
        response.raise_for_status()

        json = response.json()
        if not isinstance(json, dict):
            raise TypeError()

        return json
