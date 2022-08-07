from .. import Middleware as Middleware
from ...request.request import Request
from typing import Any

class GuardMiddleware(Middleware):
    def before(self, request: Request, _: Any, guard: str) -> Request: ...
    def after(self, request: Request, _: Any, __: Any) -> Request: ...
