from ...commands.Command import Command as Command
from ...utils.filesystem import get_module_dir as get_module_dir, make_directory as make_directory, render_stub_file as render_stub_file
from ...utils.location import base_path as base_path
from ...utils.str import as_filepath as as_filepath
from _typeshed import Incomplete

class MakeNotificationCommand(Command):
    app: Incomplete
    def __init__(self, application) -> None: ...
    def handle(self): ...
    def get_stub_notification_path(self): ...
