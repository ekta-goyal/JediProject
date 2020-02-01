from flask import request, redirect, url_for, render_template, current_app, Blueprint
from app.workforceapp.models import User, Team
from flask_login import logout_user, login_user
from flask_admin import Admin
from app.workforceapp.view import AdministratorIndexView, AdministratorModelView
from app.database import db


admin_html_blueprint = Blueprint('admin_html_blueprint', __name__)
# Flask and Flask-SQLAlchemy initialization here


@admin_html_blueprint.route('/login', methods=['POST'])
def admin_login():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username, password=password).first()
    try:
        login_user(user)
    except AttributeError:
        return redirect(url_for('admin.index', error="No records found"))
    else:
        return redirect(url_for('admin.index'))


@admin_html_blueprint.route('/logout', methods=['GET'])
def admin_logout():
    logout_user()
    return redirect(url_for('admin.index'))


extra_css = [
        'https://stackpath.bootstrapcdn.com/bootswatch/3.3.5/flatly/bootstrap.min.css',
        "https://fonts.googleapis.com/css?family=Megrim&display=swap",
        '/static/css/main-admin.css'
]

admin_index_view = AdministratorIndexView(
        template='adminapp/index.html'
    )
admin_index_view.add_extra_css(extra_css)
admin = Admin(
    name='Admin Task Manager',
    template_mode='bootstrap3',
    index_view=admin_index_view
)

user = AdministratorModelView(User, db.session)
user.add_extra_css(extra_css)
admin.add_view(user)

#admin.add_view(AdministratorModelView(Team, db.session))