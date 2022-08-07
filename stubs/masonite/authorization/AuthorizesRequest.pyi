from ..facades import Gate as Gate
from .AuthorizationResponse import AuthorizationResponse
from typing import Any

class AuthorizesRequest:
    def authorize(self, permission: str, *args: Any) -> AuthorizationResponse: ...
