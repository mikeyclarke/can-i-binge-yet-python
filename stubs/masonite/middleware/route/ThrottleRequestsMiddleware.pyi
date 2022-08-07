from ...exceptions import ThrottleRequestsException as ThrottleRequestsException
from ...facades import RateLimiter as RateLimiter
from ...rates.Limit import Limit as Limit
from ...request import Request as Request
from ...response import Response as Response
from ..middleware import Middleware as Middleware
from attr import has as has

class ThrottleRequestsMiddleware(Middleware):
    def before(self, request: Request, response: Response, limit_string: str) -> Request: ...
    def after(self, request: Request, response: Response, limit_string: str) -> Request: ...
    def get_headers(self, key: str, max_attempts: int, limited: bool = ...) -> dict[str, str | int]: ...
