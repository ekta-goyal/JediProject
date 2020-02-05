from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from flask_login import current_user
from wtforms.validators import DataRequired

from .util import TimeManager, ExtraCss
from flask_admin.form import SecureForm

class UserView(ModelView, ExtraCss, TimeManager):
    column_exclude_list = ('password',)
    column_labels = dict(name='Name', username="Username(email)")
    column_searchable_list = ('name',)
    column_filters = ('type',) 

    form_excluded_columns = ('as_assignee','as_reporter', 'teams', 'is_verified', 'password') + TimeManager.form_excluded_columns
    
    column_list = ['id', 'name', 'username', 'created_at', 'modified_at']

    form_base_class = SecureForm
    
    form_args = dict(
        name=dict(label='Name', validators=[DataRequired()]),
        type=dict(label='User Type', validators=[DataRequired()])
    )

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_html_blueprint.admin_login'))