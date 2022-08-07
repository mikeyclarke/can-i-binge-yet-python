from ...authentication import Auth as Auth
from ...controllers import Controller as Controller
from ...request import Request as Request
from ...response import Response as Response
from ..facades import Api as Api

class AuthenticationController(Controller):
    def auth(self, auth: Auth, request: Request, response: Response): ...
    def reauth(self, request: Request, response: Response): ...
