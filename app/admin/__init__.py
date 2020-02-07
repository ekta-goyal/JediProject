from models import User
from models import Team
from flask_admin import Admin
from flask import url_for
from app.database import db

from .controller import AdministratorIndexView, UserView, TeamView, AddTeamView
from .controller import admin_html_blueprint


admin_index_view = AdministratorIndexView(
        template='index.html',
    )


admin = Admin(
    name='Admin Task Manager',
    template_mode='bootstrap3',
    index_view=admin_index_view
)

#admin.add_view(AdministratorModelView(Team, db.session))


def init_admin(app):
    with app.app_context():
        admin.init_app(app)
        extra_css = [
                '/admin/view.static/css/main-admin.css'
        ]
        admin_index_view.add_extra_css(extra_css)
        user = UserView(User, db.session)
        user.add_extra_css(extra_css)
        admin.add_view(user)

        team = TeamView(Team, db.session)
        team.add_extra_css(extra_css)
        admin.add_view(team)
