from masonite.routes import Route

ROUTES = [
    Route.get('/', 'HomeController@show').name('home'),
]
