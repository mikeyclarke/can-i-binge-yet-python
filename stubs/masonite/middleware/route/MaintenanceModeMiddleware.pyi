from .. import Middleware as Middleware
from ...request import Request
from ...response import Response
from typing import Any

class MaintenanceModeMiddleware(Middleware):
    def before(self, request: Request, response: Response) -> Request | Response | bytes: ...
    def after(self, request: Request, _: Any) -> Request: ...
