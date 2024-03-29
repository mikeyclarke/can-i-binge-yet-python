from ..utils.filesystem import get_module_dir as get_module_dir, make_full_directory as make_full_directory
from ..utils.location import base_path as base_path, resources_path as resources_path

class Preset:
    key: str
    packages: dict[str, str]
    removed_packages: list[str]
    def get_base_stubs_directory(self) -> str: ...
    def get_stubs_directory(self) -> str: ...
    def get_base_template_path(self, template: str) -> str: ...
    def get_template_path(self, template: str) -> str: ...
    def update_webpack_mix(self) -> None: ...
    def update_packages(self, dev: bool = ...) -> None: ...
    def update_css(self) -> None: ...
    def update_js(self) -> None: ...
    def remove_node_modules(self) -> None: ...
