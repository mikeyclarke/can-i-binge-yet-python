from masonite.foundation import Application
from masonite.commands import Command
from typing import Any

class TaskHandler:
    tasks: list[Command]
    application: Application
    def __init__(self, application: Application, tasks: list[Command] | None = ...) -> None: ...
    def add(self, *tasks: list[Any]) -> None: ...
    def run(self, run_name: str | None = ..., force: bool = ...) -> None: ...
