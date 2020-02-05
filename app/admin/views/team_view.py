from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from flask_login import current_user
from wtforms.validators import DataRequired

from .util import TimeManager, ExtraCss
from flask_admin.form import SecureForm

class TeamView(ModelView, ExtraCss, TimeManager):
    column_labels = dict(name='Name')
    column_searchable_list = ('name', 'description')

    form_excluded_columns = ('tasks',) + TimeManager.form_excluded_columns

    column_list = ['id', 'name', 'description', 'created_at', 'modified_at']
        
    form_args = dict(
        name = dict(label='Name', validators=[DataRequired()]),
        description = dict(label='Description', validators=[DataRequired()])
    )

    form_base_class = SecureForm

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):    
        return redirect(url_for('admin_html_blueprint.admin_login'))