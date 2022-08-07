from ..views.view import View
from typing import Any

class ViewController:
    template: str
    data: dict[Any, Any]
    def __init__(self, template: str, data: dict[Any, Any]) -> None: ...
    def show(self) -> View: ...
