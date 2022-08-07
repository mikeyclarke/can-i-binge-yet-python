from ..foundation.Application import Application
from .Command import Command as Command

class ServeCommand(Command):
    app: Application
    def __init__(self, application: Application) -> None: ...
    def handle(self) -> None: ...
