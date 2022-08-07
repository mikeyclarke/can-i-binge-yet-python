from ...foundation.Application import Application
from ...response.response import Response
from typing import Protocol


class HttpException(Protocol):
    def get_response(self) -> str: ...
    def get_status(self) -> int: ...


class HttpExceptionHandler:
    application: Application
    def __init__(self, application: Application) -> None: ...
    def handle(self, exception: HttpException) -> str | bytes | Response: ...
