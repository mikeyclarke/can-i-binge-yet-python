from typing import Union

class Recipient:
    recipient: str
    def __init__(self, recipient: str | list[str] | tuple[str]) -> None: ...
    def header(self) -> str: ...
