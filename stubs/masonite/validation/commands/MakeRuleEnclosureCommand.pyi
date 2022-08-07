from ...commands.Command import Command as Command
from ...foundation import Application
from ...utils.filesystem import get_module_dir as get_module_dir, make_directory as make_directory, render_stub_file as render_stub_file
from ...utils.location import base_path as base_path
from ...utils.str import as_filepath as as_filepath

class MakeRuleEnclosureCommand(Command):
    app: Application
    def __init__(self, application: Application) -> None: ...
    def handle(self) -> int | None: ...
    def get_stub_rule_enclosure_path(self) -> str: ...
