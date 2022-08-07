from .Facade import Facade as Facade

class Session(metaclass=Facade):
    key: str
