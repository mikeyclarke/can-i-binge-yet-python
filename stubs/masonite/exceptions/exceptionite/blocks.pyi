from ...helpers import optional as optional
from ...utils.str import get_controller_name as get_controller_name
from exceptionite import Block # type: ignore

def recursive_serializer(data): ...

class AppBlock(Block):
    id: str
    name: str
    icon: str
    has_sections: bool
    def build(self): ...

class RequestBlock(Block):
    id: str
    name: str
    icon: str
    has_sections: bool
    def build(self): ...

class ConfigBlock(Block):
    id: str
    name: str
    icon: str
    has_sections: bool
    def build(self): ...
