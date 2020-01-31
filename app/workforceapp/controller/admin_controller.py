from flask import request, redirect, url_for, render_template, Blueprint
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
    user = User.query.filter_by(name=username, password=password).first()
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


admin = Admin(
    name='Admin Task Manager',
    template_mode='bootstrap3',
    index_view=AdministratorIndexView(
        template='adminapp/index.html'
    )
)
admin.add_view(AdministratorModelView(User, db.session))
#admin.add_view(AdministratorModelView(Team, db.session))