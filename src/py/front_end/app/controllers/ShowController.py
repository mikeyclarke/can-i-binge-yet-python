from masonite.controllers import Controller
from masonite.request import Request
from masonite.views import View
from src.py.show import ShowPageResult
from typing import Any


class ShowController(Controller):
    def __init__(self, view: View) -> None:
        self.__view = view

    def show(self, request: Request) -> View:
        show: ShowPageResult = request.param('show')

        context: dict[str, Any] = {
            'html_title': show['title'],
            'show': show,
        }

        return self.__view.render('show', context)
