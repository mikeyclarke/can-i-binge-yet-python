from ..request import Request as Request
from ..response import Response as Response
from .Application import Application as Application
from typing import Any, Callable, Iterator, List, Tuple

ResponseHandler = Callable[[str, List[Tuple[Any]]], None]

def response_handler(environ: dict[str, Any], start_response: ResponseHandler) -> Iterator[bytes]: ...
def testcase_handler(application: Application, environ: dict[str, Any], start_response: ResponseHandler, exception_handling: bool = ...) -> Tuple[Request, Response]: ...
