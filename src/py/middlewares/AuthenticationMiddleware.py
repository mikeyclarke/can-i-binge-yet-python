from masonite.middleware import Middleware
from masonite.request import Request
from masonite.response import Response


class AuthenticationMiddleware(Middleware):
    """Middleware to check if the user is logged in."""

    def before(self, request: Request, response: Response) -> Request:
        if not request.user():
            return response.redirect(name="login")
        return request

    def after(self, request: Request, response: Response) -> Request:
        return request
