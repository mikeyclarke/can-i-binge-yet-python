from .AuthorizationResponse import AuthorizationResponse as AuthorizationResponse

class Policy:
    def allow(self, message: str = ..., code: int | None = ...) -> AuthorizationResponse: ...
    def deny(self, message: str = ..., code: int | None = ...) -> AuthorizationResponse: ...
