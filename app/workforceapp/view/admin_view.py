from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app.workforceapp.models import User
from flask import redirect, url_for, current_app
from wtforms.validators import DataRequired

class AdministratorIndexView(AdminIndexView):
    extra_css = []

    def add_extra_css(this, css):
        this.extra_css.extend(css)

class AdministratorModelView(ModelView):
    column_exclude_list = ('password')

    column_labels = dict(name='Name', modified="Modified At")

    column_searchable_list = ('name',)

    column_default_sort = [('modified', True), ('created_at', True)]

    column_filters = ('type',)

    form_excluded_columns = ('deleted_at', 'created_at', 'modified', 'is_verified')

    extra_css = []

    def add_extra_css(this, css):
        this.extra_css.extend(css)
        
    form_args = dict(
        name=dict(label='Name', validators=[DataRequired()]),
        type=dict(label='User Type', validators=[DataRequired()])
    )

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login'))