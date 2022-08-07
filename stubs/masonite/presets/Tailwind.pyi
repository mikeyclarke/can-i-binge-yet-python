from ..utils.filesystem import make_full_directory as make_full_directory
from ..utils.location import base_path as base_path, resources_path as resources_path
from .Preset import Preset as Preset
from _typeshed import Incomplete

class Tailwind(Preset):
    key: str
    packages: Incomplete
    def install(self) -> None: ...
    def add_tailwind_config(self) -> None: ...
    def update_css(self) -> None: ...
