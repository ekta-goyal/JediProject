from flask_admin import AdminIndexView
from flask_login import current_user
from flask import redirect, url_for

from .util import ExtraCss

class AdministratorIndexView(AdminIndexView, ExtraCss):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.type == 'regular-user':
            return False
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('html_blueprint.index', error="Please Logout from current user"))
