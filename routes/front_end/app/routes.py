from src.py.front_end.app.controllers import HomeController, ShowController
from masonite.routes import Route

FRONT_END_APP_ROUTES = [
    Route.group(
        [
            Route.get('/', HomeController.show).name('home'),
            Route.get('/show/@show_url_path', ShowController.show).name('show').middleware('show_loader'),
        ],
        name = 'front_end.app.',
    ),
]
