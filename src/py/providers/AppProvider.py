from masonite.foundation import Application
from masonite.providers import Provider


class AppProvider(Provider):
    def __init__(self, application: Application) -> None:
        self.application = application

    def register(self) -> None:
        pass

    def boot(self) -> None:
        pass
