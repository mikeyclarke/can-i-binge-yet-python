from ..validation.MessageBag import MessageBag
from ..validation.RuleEnclosure import RuleEnclosure

class ValidatesRequest:
    def validate(self, *rules: str | dict[str, str] | RuleEnclosure) -> MessageBag: ...
