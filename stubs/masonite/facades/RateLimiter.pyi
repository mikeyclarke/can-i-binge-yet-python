from .Facade import Facade as Facade

class RateLimiter(metaclass=Facade):
    key: str
