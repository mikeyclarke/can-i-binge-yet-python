from ...controllers import Controller as Controller
from ...request import Request as Request
from ...response import Response as Response

class ExceptioniteController(Controller):
    def run_action(self, request: Request, response: Response): ...
