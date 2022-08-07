from .Task import Task as Task
from _typeshed import Incomplete

class CommandTask(Task):
    run_every_minute: bool
    command: Incomplete
    def __init__(self, command: str = ...) -> None: ...
    def handle(self) -> None: ...
