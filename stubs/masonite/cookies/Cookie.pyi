from typing import Optional

class Cookie:
    name: str
    value: str
    http_only: bool
    secure: bool
    expires: Optional[str]
    timezone: Optional[str]
    samesite: str
    path: str
    def __init__(self, name: str, value: str, expires: Optional[str] = ..., http_only: bool = ..., path: str = ..., timezone: Optional[str] = ..., secure: bool = ..., samesite: str = ...) -> None: ...
    def render(self) -> str: ...
