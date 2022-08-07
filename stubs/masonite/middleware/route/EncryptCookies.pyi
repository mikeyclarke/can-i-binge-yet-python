from ...request.request import Request
from ...response.response import Response
from typing import Optional

class EncryptCookies:
    def before(self, request: Request, response: Response) -> Optional[Request]: ...
    def after(self, request: Request, response: Response) -> Optional[Request]: ...
