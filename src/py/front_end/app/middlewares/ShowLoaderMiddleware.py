from masonite.exceptions import RouteNotFoundException
from masonite.middleware import Middleware
from masonite.request import Request
from masonite.response import Response
from src.py.show import ShowLoader
import re


class ShowLoaderMiddleware(Middleware):
    def __init__(self, show_loader: ShowLoader) -> None:
        self.__show_loader = show_loader

    def before(self, request: Request, response: Response) -> Request | Response:
        show_url_path = request.param('show_url_path')

        re_match = re.search('^([0-9]+)-', show_url_path)
        if re_match is None:
            raise RouteNotFoundException('')

        id = re_match.group(1)
        slug = show_url_path[len(id) + 1:]

        if len(slug) == 0:
            raise RouteNotFoundException('')

        show = self.__show_loader.load(int(id))
        if show is None:
            raise RouteNotFoundException('')

        if slug != show['slug']:
            return response.redirect(name='show', params={
                'show_url_path': show['url_path']
            })

        request.load_params({
            'show': show,
        })

        return request

    def after(self, request: Request, response: Response) -> Request:
        return request
