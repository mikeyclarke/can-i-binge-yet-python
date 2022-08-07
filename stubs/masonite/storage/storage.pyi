from typing import TypeVar

STORAGE_TEMPLATES = dict[str, str]

T = TypeVar('T', bound=StorageCapsule)

class StorageCapsule:
    storage_templates: STORAGE_TEMPLATES
    def __init__(self) -> None: ...
    def add_storage_assets(self, templates: STORAGE_TEMPLATES) -> T: ...
    def get_storage_assets(self) -> STORAGE_TEMPLATES: ...
