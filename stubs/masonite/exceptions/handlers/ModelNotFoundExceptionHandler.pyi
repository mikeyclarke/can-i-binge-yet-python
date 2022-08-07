from ...foundation.Application import Application


class ModelNotFoundHandler:
    application: Application
    def __init__(self, application: Application) -> None: ...
    def handle(self, exception: Exception) -> None: ...
