from ..utils.location import base_path as base_path, resources_path as resources_path
from .Preset import Preset as Preset
from _typeshed import Incomplete

class Remove(Preset):
    key: str
    removed_packages: Incomplete
    def install(self) -> None: ...
    def remove_all_presets_file(self) -> None: ...
