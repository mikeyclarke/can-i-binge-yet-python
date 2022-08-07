from .Facade import Facade as Facade

class Request(metaclass=Facade):
    key: str
