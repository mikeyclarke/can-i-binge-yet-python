from ..facades import Api as Api

class AuthenticatesTokens:
    __TOKEN_COLUMN__: str
    def generate_jwt(self): ...
    def attempt_by_token(self, token): ...
