from masonite.foundation import Application, response_handler
from masonite.storage import StorageCapsule
from masonite.auth import Sign
from masonite.environment import LoadEnvironment
from masonite.utils.structures import load
from masonite.utils.location import base_path
from masonite.middleware import (
    SessionMiddleware,
    EncryptCookies,
    LoadUserMiddleware,
    MaintenanceModeMiddleware,
)
from masonite.routes import Route, HTTPRoute
from masonite.configuration.Configuration import Configuration
from masonite.configuration import config
from typing import cast

from src.py.middlewares import VerifyCsrfToken, AuthenticationMiddleware


class Kernel:

    http_middleware = [MaintenanceModeMiddleware, EncryptCookies]

    route_middleware = {
        'web': [SessionMiddleware, LoadUserMiddleware, VerifyCsrfToken],
        'auth': [AuthenticationMiddleware],
    }

    def __init__(self, app: Application) -> None:
        self.application = app

    def register(self) -> None:
        # Register routes
        self.load_environment()
        self.register_configurations()
        self.register_middleware()
        self.register_routes()
        self.register_database()
        self.register_templates()
        self.register_storage()

    def load_environment(self) -> None:
        LoadEnvironment()

    def register_configurations(self) -> None:
        # load configuration
        self.application.bind('config.location', 'config')
        configuration = Configuration(self.application)
        configuration.load()
        self.application.bind('config', configuration)
        key = config('application.key')
        self.application.bind('key', key)
        self.application.bind('sign', Sign(key))
        # set locations
        self.application.bind('controllers.location', '')
        self.application.bind('resources.location', '')
        self.application.bind('jobs.location', 'src/py/jobs')
        self.application.bind('providers.location', 'src/py/providers')
        self.application.bind('mailables.location', 'src/py/mailables')
        self.application.bind('listeners.location', 'src/py/listeners')
        self.application.bind('validation.location', 'src/py/validation')
        self.application.bind('notifications.location', 'src/py/notifications')
        self.application.bind('events.location', 'src/py/events')
        self.application.bind('tasks.location', 'src/py/tasks')
        self.application.bind('models.location', 'src/py/models')
        self.application.bind('observers.location', 'src/py/models/observers')
        self.application.bind('policies.location', 'src/py/policies')
        self.application.bind('commands.location', 'src/py/commands')
        self.application.bind('middlewares.location', 'src/py/middlewares')

        self.application.bind('server.runner', 'masonite.commands.ServeCommand.main')

    def register_middleware(self) -> None:
        self.application.make('middleware').add(self.route_middleware).add(self.http_middleware)

    def register_routes(self) -> None:
        Route.set_controller_locations('src/py/front_end/app/controllers')
        self.application.bind('routes.location', 'routes/web')
        routes = load(self.application.make('routes.location'), 'ROUTES')
        routes = cast(list[HTTPRoute], routes)
        self.application.make('router').add(
            Route.group(
                routes, middleware=['web']
            )
        )

    def register_database(self) -> None:
        from masoniteorm.query import QueryBuilder # type: ignore

        self.application.bind(
            'builder',
            QueryBuilder(connection_details=config('database.databases')),
        )

        self.application.bind('migrations.location', '')
        self.application.bind('seeds.location', '')

        self.application.bind('resolver', config('database.db'))

    def register_templates(self) -> None:
        self.application.bind('views.location', 'ui/jinja/')

    def register_storage(self) -> None:
        storage = StorageCapsule()
        storage.add_storage_assets(config('filesystem.staticfiles'))
        self.application.bind('storage_capsule', storage)

        self.application.set_response_handler(response_handler)
        self.application.use_storage_path(base_path('storage'))
