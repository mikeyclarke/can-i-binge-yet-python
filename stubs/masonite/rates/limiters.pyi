from ..request import Request as Request
from .Limit import Limit as Limit
from typing import Optional

class Limiter:
    def __init__(self) -> None: ...
    def allow(self, request: Request) -> Optional[Limit]: ...

class GlobalLimiter(Limiter):
    limit: str
    def __init__(self, limit: str) -> None: ...
    def allow(self, request: Request) -> Limit: ...

class UnlimitedLimiter(Limiter):
    def allow(self, request: Request) -> Limit: ...

class GuestsOnlyLimiter(Limiter):
    limit: str
    def __init__(self, limit: str) -> None: ...
    def allow(self, request: Request) -> Limit: ...
