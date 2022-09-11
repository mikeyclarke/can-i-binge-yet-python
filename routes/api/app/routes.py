from src.py.api.app.controllers import SeasonEpisodesController
from masonite.routes import Route

API_APP_ROUTES = [
    Route.group(
        [
            Route.get('/show/@show_id/season-episodes/@season_number', SeasonEpisodesController.get).name('season_episodes.get'),
        ],
        prefix = '/_',
        name = 'api.app.',
    ),
]
