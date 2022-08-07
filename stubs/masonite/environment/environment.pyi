from os import PathLike
from typing import Any, Callable, IO, Optional

LoadDotenv = Callable[
    [
        Optional[str | PathLike],
        Optional[IO[str]],
        bool,
        bool,
        bool,
        Optional[str]
    ],
    bool
]

class LoadEnvironment:
    env: LoadDotenv
    def __init__(self, environment: Optional[str] = ..., override: bool = ..., only: Optional[str] = ...) -> None: ...

def env(value: str, default: str = ..., cast: bool = ...) -> Any: ...
