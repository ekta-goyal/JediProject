from flask_admin import BaseView, expose

from .util import ExtraCss

class AddTeamView(BaseView):
    @expose('/')
    def index(self):
        return self.render('adminapp/notify.html')