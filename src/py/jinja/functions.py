from masonite.request import Request
from markupsafe import Markup
from urllib.parse import urlparse
from typing import Optional


def return_to_url(request: Request, fallback_url: str) -> str:
    return_to = request.input('return_to', None)
    if return_to is None:
        return fallback_url

    try:
        parsed_url = urlparse(return_to)
    except ValueError:
        return fallback_url

    if parsed_url.scheme != '' or parsed_url.netloc != '' or not parsed_url.path.startswith('/'):
        return fallback_url

    return return_to


def icon(name: str, class_name: str, label: Optional[str] = None) -> str:
    aria_attribute = 'aria-hidden="true"' if label is None else f'aria-label="{label}"'
    return Markup(f'<svg class="{class_name}" {aria_attribute}><use xlink:href="#icon-sprite__{name}"/></svg>')
