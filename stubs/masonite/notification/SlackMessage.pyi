from _typeshed import Incomplete

class SlackMessage:
    WEBHOOK_MODE: int
    API_MODE: int
    def __init__(self) -> None: ...
    def from_(self, username, icon: Incomplete | None = ..., url: Incomplete | None = ...): ...
    def to(self, to): ...
    def text(self, text): ...
    def link_names(self): ...
    def unfurl_links(self): ...
    def without_markdown(self): ...
    def can_reply(self): ...
    def build(self, *args, **kwargs): ...
    def get_options(self): ...
    def token(self, token): ...
    def as_current_user(self): ...
    def webhook(self, webhook): ...
    def block(self, block_instance): ...
    def mode(self, mode): ...
