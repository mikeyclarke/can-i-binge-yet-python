from ...configuration import config as config
from ...providers import Provider as Provider
from ...utils.structures import load as load
from ..MockNotification import MockNotification as MockNotification
from ..NotificationManager import NotificationManager as NotificationManager
from ..commands import MakeNotificationCommand as MakeNotificationCommand, NotificationTableCommand as NotificationTableCommand
from ..drivers import BroadcastDriver as BroadcastDriver, DatabaseDriver as DatabaseDriver, MailDriver as MailDriver, SlackDriver as SlackDriver, VonageDriver as VonageDriver
from _typeshed import Incomplete

class NotificationProvider(Provider):
    application: Incomplete
    def __init__(self, application) -> None: ...
    def register(self) -> None: ...
    def boot(self) -> None: ...
