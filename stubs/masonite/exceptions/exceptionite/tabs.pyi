from exceptionite import Tab # type: ignore
from typing import Any

class DumpsTab(Tab):
    id: str
    name: str
    component: str
    icon: str
    advertise_content: bool
    empty_msg: str
    def build(self) -> dict[str, Any]: ...
    def has_content(self) -> bool: ...
