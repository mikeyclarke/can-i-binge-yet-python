from typing import Any

class Pipeline:
    payload: Any
    args: Any
    def __init__(self, payload: Any, *args: Any) -> None: ...
    def through(self, pipe_list: list[object], handler: str = ...) -> bool: ...
