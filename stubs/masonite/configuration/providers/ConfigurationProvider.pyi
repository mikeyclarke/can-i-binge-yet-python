from ...foundation.Application import Application
from ...providers.Provider import Provider

class ConfigurationProvider(Provider):
    application: Application
    def __init__(self, application: Application) -> None: ...
    def register(self) -> None: ...
    def boot(self) -> None: ...
