from .Command import Command

BANNER: str

class TinkerCommand(Command):
    def handle(self) -> None: ...
