from .SeasonEpisodesFormatter import SeasonEpisodesFormatter, SeasonEpisode
from src.py.themoviedb import TheMovieDbClient
from requests import HTTPError
from typing import Any


class SeasonEpisodesLoader:
    def __init__(self, season_episodes_formatter: SeasonEpisodesFormatter, tmdb_client: TheMovieDbClient) -> None:
        self.__season_episodes_formatter = season_episodes_formatter
        self.__tmdb_client = tmdb_client

    def load(self, show_id: int, season_number: int) -> list[SeasonEpisode] | None:
        try:
            season = self.__tmdb_client.get_show_season(show_id, season_number)
        except HTTPError as err:
            if err.response.status_code == 404:
                return None
            raise

        formatted = self.__season_episodes_formatter.format(season['episodes'])

        return formatted
