from masonite.facades import Dump
from masonite.foundation import Application
from masonite.providers import Provider
from masonite.views import View
from src.py.asset import AssetRenderer
from src.py.jinja.filters import format_date
from src.py.jinja.functions import icon, return_to_url


class AppProvider(Provider):
    def __init__(self, application: Application) -> None:
        self.application = application

    def register(self) -> None:
        asset_renderer = self.application.make(AssetRenderer)
        view = self.application.make(View)

        view.filter('format_date', format_date)
        view.add_extension('jinja2.ext.do')
        view.share(
            {
                'icon': icon,
                'return_to_url': return_to_url,
                'get_asset_html': asset_renderer.get_asset_html,
            }
        )

        self.application.bind('view', view)

    def boot(self) -> None:
        pass
