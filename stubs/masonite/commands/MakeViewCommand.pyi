from ..foundation.Application import Application
from ..utils.filesystem import get_module_dir as get_module_dir, make_directory as make_directory, render_stub_file as render_stub_file
from ..utils.location import views_path as views_path
from .Command import Command as Command

class MakeViewCommand(Command):
    app: Application
    def __init__(self, application: Application) -> None: ...
    def handle(self) -> int | None: ...
    def get_view_path(self) -> str: ...
