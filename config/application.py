from masonite.environment import env


KEY = env('APP_KEY', '-RkDOqXojJIlsF_I8wWiUq_KRZ0PtGWTOZ676u5HtLg=')

DEBUG = env('APP_DEBUG', True)

HASHING = {
    'default': env('HASHING_FUNCTION', 'bcrypt'),
    'bcrypt': {'rounds': 10},
    'argon2': {'memory': 1024, 'threads': 2, 'time': 2},
}

APP_URL = env('APP_URL', 'http://localhost:8000/')

MIX_BASE_URL = env('MIX_BASE_URL', None)

ASSET_MANIFEST_PATH = 'public/compiled/manifest.json'

TMDB_API_BASE_URL = env('TMDB_API_BASE_URL', 'https://api.themoviedb.org')
TMDB_API_KEY = env('TMDB_API_KEY', None)

SEARCH_INPUT_PLACEHOLDER_EXAMPLE = env('SEARCH_INPUT_PLACEHOLDER_EXAMPLE', 'Stranger Things')

SNOWFALL = True
