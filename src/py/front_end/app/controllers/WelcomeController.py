from masonite.views import View
from masonite.controllers import Controller


class WelcomeController(Controller):

    def show(self, view: View) -> str:
        return view.render('welcome')
