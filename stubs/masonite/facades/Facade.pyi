from typing import Any

class Facade(type):
    def __getattr__(self, attribute: str, *args: Any, **kwargs: Any) -> Any: ...
