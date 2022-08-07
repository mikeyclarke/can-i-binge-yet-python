from .. import Middleware as Middleware
from ...request import Request
from typing import Any

class LoadUserMiddleware(Middleware):
    def before(self, request: Request, _: Any) -> Request: ...
    def after(self, request: Request, _: Any) -> Request: ...
