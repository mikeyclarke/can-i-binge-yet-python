from datetime import date, datetime
from babel.core import Locale
from babel.dates import format_date as babel_format_date, LC_TIME
from typing import Optional


def format_date(value: Optional[str | date | datetime], format: str = 'medium', locale: Optional[str | Locale] = LC_TIME) -> str:
    if isinstance(value, str):
        value = date.fromisoformat(value)

    return babel_format_date(value, format, locale)
