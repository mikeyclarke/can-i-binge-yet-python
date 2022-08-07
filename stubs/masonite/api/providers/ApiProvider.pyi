from ...configuration.helpers import config as config
from ...providers import Provider as Provider
from ...routes import Route as Route
from ...utils.structures import load as load
from ..Api import Api as Api
from ..commands.APIInstallCommand import APIInstallCommand as APIInstallCommand
from ..guards import JWTGuard as JWTGuard
from _typeshed import Incomplete

class ApiProvider(Provider):
    application: Incomplete
    def __init__(self, application) -> None: ...
    def register(self) -> None: ...
    def boot(self) -> None: ...
