from ..utils.filesystem import make_full_directory as make_full_directory
from ..utils.location import resources_path as resources_path
from .Preset import Preset as Preset
from _typeshed import Incomplete

class Bootstrap(Preset):
    key: str
    packages: Incomplete
    def install(self) -> None: ...
    def update_css(self) -> None: ...
