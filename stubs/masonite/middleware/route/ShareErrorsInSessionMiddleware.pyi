from .. import Middleware as Middleware
from ...request.request import Request
from typing import Any

class ShareErrorsInSessionMiddleware(Middleware):
    def before(self, request: Request, _: Any) -> Request: ...
    def after(self, request: Request, _: Any) -> Request: ...
