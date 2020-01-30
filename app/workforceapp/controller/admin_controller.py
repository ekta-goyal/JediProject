from flask import request, render_template,Blueprint
from app.workforceapp.models import User,Team
from flask_login import logout_user,login_user
from flask_admin import Admin
from app.workforceapp.view import AdministratorIndexView,AdministratorModelView
from app.database import db


admin_html_blueprint = Blueprint('admin_html_blueprint',__name__)
# Flask and Flask-SQLAlchemy initialization here
admin = Admin(name='Admin Task Manager', template_mode='bootstrap3', index_view=AdministratorIndexView())
admin.add_view(AdministratorModelView(User, db.session))
admin.add_view(AdministratorModelView(Team, db.session))


@admin_html_blueprint.route('/login', methods=['GET','POST'])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(name=username,password=password).first()
        print(user)
        login_user(user)
    else:
        return render_template('adminapp/login.html')


    return 'Login'

@admin_html_blueprint.route('/logout')
def admin_logout():
    logout_user()
    return 'Logout'
