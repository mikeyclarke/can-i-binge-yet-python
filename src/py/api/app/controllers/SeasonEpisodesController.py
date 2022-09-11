from masonite.controllers import Controller
from masonite.exceptions import RouteNotFoundException
from masonite.request import Request
from masonite.views import View
from src.py.show import SeasonEpisodesLoader
from typing import Any


class SeasonEpisodesController(Controller):
    def __init__(self, season_episodes_loader: SeasonEpisodesLoader, view: View) -> None:
        self.__season_episodes_loader = season_episodes_loader
        self.__view = view

    def get(self, request: Request) -> dict[str, Any]:
        show_id = request.param('show_id')
        season_number = request.param('season_number')

        episodes = self.__season_episodes_loader.load(show_id, season_number)
        if episodes is None:
            raise RouteNotFoundException('')

        template = self.__view.render('show/_season_episodes', {
            'season': {
                'episodes': episodes,
            }
        })

        return {'html': template.get_content()}
