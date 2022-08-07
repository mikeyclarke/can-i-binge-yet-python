from ..response import Response as Response

class RedirectController:
    url: str
    status: int
    def __init__(self, url: str, status: int) -> None: ...
    def redirect(self, response: Response) -> Response: ...
