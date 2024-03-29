from masoniteorm.models import Model

class Authenticates:
    __auth__: str
    __password__: str
    def attempt(self, username: str, password: str) -> bool | Model | None: ...
    def get_auth_column(self, username: str) -> bool | str: ...
    def register(self, dictionary: dict[str, str]) -> Model: ...
    def get_id(self) -> str | int: ...
    def attempt_by_id(self, user_id: int | str) -> Model: ...
    def get_remember_token(self) -> str: ...
    remember_token: str
    def set_remember_token(self, token: str | None = ...) -> Authenticates: ...
    def reset_password(self, username: str, password: str) -> Authenticates: ...
    def get_password_column(self) -> str: ...
    def get_username_column(self) -> str: ...
