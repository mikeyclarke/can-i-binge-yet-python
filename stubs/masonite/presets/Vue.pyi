from ..utils.filesystem import make_directory as make_directory
from ..utils.location import resources_path as resources_path, views_path as views_path
from .Preset import Preset as Preset
from _typeshed import Incomplete

class Vue(Preset):
    key: str
    packages: Incomplete
    removed_packages: Incomplete
    def install(self) -> None: ...
    def add_components(self) -> None: ...
    def create_view(self) -> None: ...
