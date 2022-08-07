from ..request.request import Request
from typing import Any

class MustVerifyEmail:
    def verify_email(self, mail_manager: Any, request: Request) -> None: ...
