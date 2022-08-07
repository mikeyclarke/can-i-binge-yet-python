from ...request.request import Request
from ...response.response import Response
from .. import Middleware as Middleware

class ClearDumpsBetweenRequestsMiddleware(Middleware):
    def before(self, request: Request, response: Response) -> Response: ...
    def after(self, request: Request, response: Response) -> Response: ...
