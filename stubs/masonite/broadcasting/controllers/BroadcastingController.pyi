from ...controllers import Controller as Controller
from ...request import Request as Request
from ..Broadcast import Broadcast as Broadcast

class BroadcastingController(Controller):
    def authorize(self, request: Request, broadcast: Broadcast): ...
