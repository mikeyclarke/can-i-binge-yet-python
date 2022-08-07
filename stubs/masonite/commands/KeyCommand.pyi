from .Command import Command as Command

class KeyCommand(Command):
    def handle(self) -> None: ...
