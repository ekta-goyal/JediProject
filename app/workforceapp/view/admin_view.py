from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app.workforceapp.models import User
from flask import redirect


class AdministratorIndexView(AdminIndexView):
    def is_accessible(self):
        from app.loginmanager import login_manager
        @login_manager.user_loader
        def load_admin(user_id):
            return User.query.get(user_id)
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/admin/login')

class AdministratorModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        pass  # return redirect(url_for('admin_login'))