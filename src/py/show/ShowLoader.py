from .ShowPageFormatter import ShowPageFormatter, ShowPageResult
from src.py.themoviedb import TheMovieDbClient
from requests import HTTPError
from typing import Any


class ShowLoader:
    def __init__(self, show_page_formatter: ShowPageFormatter, tmdb_client: TheMovieDbClient) -> None:
        self.__show_page_formatter = show_page_formatter
        self.__tmdb_client = tmdb_client

    def load(self, id: int) -> ShowPageResult | None:
        try:
            show = self.__tmdb_client.get_show(id)
        except HTTPError as err:
            if err.response.status_code == 404:
                return None
            raise

        formatted = self.__show_page_formatter.format(show)

        return formatted
