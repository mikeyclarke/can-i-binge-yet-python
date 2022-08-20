from masonite.environment import env

STORES = {
    'default': 'redis',
    'local': {
        'driver': 'file',
        'location': 'storage/framework/cache',
    },
    'redis': {
        'driver': 'redis',
        'host': env('REDIS_HOST'),
        'port': env('REDIS_PORT'),
        'password': '',
        'name': 'bingeable',
    },
}
