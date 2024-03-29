from ...exceptions import NotificationException as NotificationException
from .BaseDriver import BaseDriver as BaseDriver
from _typeshed import Incomplete

class SlackDriver(BaseDriver):
    WEBHOOK_MODE: int
    API_MODE: int
    send_url: str
    channel_url: str
    application: Incomplete
    options: Incomplete
    mode: Incomplete
    def __init__(self, application) -> None: ...
    def set_options(self, options): ...
    def send(self, notifiable, notification) -> None: ...
    def build(self, notifiable, notification): ...
    def get_recipients(self, notifiable): ...
    def get_sending_mode(self, recipients): ...
    def send_via_webhook(self, slack_message) -> None: ...
    def send_via_api(self, slack_message): ...
    def convert_channel(self, name, token): ...
