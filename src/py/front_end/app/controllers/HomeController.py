from masonite.controllers import Controller
from masonite.request import Request
from masonite.views import View
from src.py.show import ShowSearch, TrendingShows
from typing import Any


class HomeController(Controller):
    def __init__(self, show_search: ShowSearch, trending_shows: TrendingShows, view: View) -> None:
        self.__show_search = show_search
        self.__trending_shows = trending_shows
        self.__view = view

    def show(self, request: Request) -> View:
        if request.input('q', None) is not None:
            return self.__show_search_view(request)

        return self.__show_home_view(request)

    def __show_home_view(self, request: Request) -> View:
        context: dict[str, Any] = {
            'trending_shows': self.__trending_shows.get_all()
        }

        return self.__view.render('home', context)

    def __show_search_view(self, request: Request) -> View:
        search_token = request.input('q')

        context: dict[str, Any] = {
            'search_token': search_token,
            'results': [],
        }

        context['results'] = self.__show_search.search(search_token)

        return self.__view.render('search', context)
