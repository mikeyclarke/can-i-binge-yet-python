from ...foundation.Application import Application
from ...providers.Provider import Provider

class PresetsProvider(Provider):
    application: Application
    def __init__(self, app: Application) -> None: ...
    def register(self) -> None: ...
    def boot(self) -> None: ...
