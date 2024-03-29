from ..foundation.Application import Application
from typing import Any, Optional, Protocol


class HandlerDriver(Protocol):
    def handle(self, exception: Exception) -> Optional[str]: ...


class ExceptionHandler:
    application: Application
    drivers: dict[str, HandlerDriver]
    driver_config: dict[str, Any]
    options: dict[str, Any]
    def __init__(self, application: Application, driver_config: Optional[dict[str, Any]] = ...) -> None: ...
    def add_driver(self, name: str, driver: HandlerDriver) -> None: ...
    def set_configuration(self, config: dict[str, Any]) -> ExceptionHandler: ...
    def get_driver(self, name: Optional[str] = ...) -> HandlerDriver: ...
    def get_config_options(self, driver: Optional[str] = ...) -> dict[str, Any]: ...
    def handle(self, exception: Exception) -> Optional[str]: ...
