from masonite.foundation import Application
from typing import Any, TypeVar

T = TypeVar('T', bound=TerminalDriver)

class TerminalDriver:
    application: Application
    options: dict[str, Any]
    content_type: str | None
    def __init__(self, application: Application) -> None: ...
    def set_options(self, options: dict[str, Any]) -> T: ...
    def send(self) -> None: ...
