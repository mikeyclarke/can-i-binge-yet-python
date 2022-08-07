from .Command import Command as Command

class InstallCommand(Command):
    def handle(self) -> None: ...
