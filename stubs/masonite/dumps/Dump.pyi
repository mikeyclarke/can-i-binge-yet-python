from typing import Any
from typing_extensions import TypedDict

def color(string: str) -> str: ...
def is_property(obj: object) -> bool: ...
def is_local(obj_name: str, obj: object) -> bool: ...
def is_private(obj_name: str) -> bool: ...
def serialize_property(obj: object) -> str | dict[str, Any]: ...


class SerializedResult(TypedDict):
    objects: dict[str, Any]
    method: str
    filename: str
    line: int
    timestamp: float


class Dump:
    objects: dict[str, Any]
    method: str
    filename: str
    line: int
    timestamp: float
    def __init__(self, objects: dict[str, Any], method: str, filename: str, line: int) -> None: ...
    def serialize(self) -> SerializedResult: ...
