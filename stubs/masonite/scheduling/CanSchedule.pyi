from .CommandTask import CommandTask
from .Task import Task

class CanSchedule:
    def call(self, command: str) -> CommandTask: ...
    def schedule(self, task: Task) -> Task: ...
