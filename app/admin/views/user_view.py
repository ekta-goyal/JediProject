from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, current_app, render_template
from flask_login import current_user
from wtforms.validators import DataRequired

from .util import TimeManager, ExtraCss
from flask_admin.form import SecureForm
from app.mail import send_async_email

class UserView(ModelView, ExtraCss, TimeManager):
    column_exclude_list = ('password',)
    column_labels = dict(name='Name', username="Username(email)")
    column_searchable_list = ('name',)
    column_filters = ('type',) 

    form_excluded_columns = ('as_assignee','as_reporter', 'teams', 'is_verified', 'password') + TimeManager.form_excluded_columns
    
    column_list = ['is_verified','id', 'name', 'username', 'contact', 'created_at', 'modified_at']

    form_base_class = SecureForm

    can_create = True
    can_delete = True
    can_edit = False

    form_args = dict(
        name=dict(label='Name', validators=[DataRequired()]),
        type=dict(label='User Type', validators=[DataRequired()])
    )

    def is_accessible(self):
        if current_user.is_authenticated and current_user.type == 'admin':
            return True
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        if current_user.type == 'user':
            return redirect(url_for('html_blueprint.index'))
        return redirect(url_for('admin_html_blueprint.admin_login'))

    def after_model_change(self, form, model, is_created):
        if is_created:
            from app.crypt import get_time_token
            token = get_time_token(model.username, salt="user-create")
            subject = "Invitation | Welcone to Jedi Order | Simple tool to track and post tasks accross organization."
            body = token
            html = render_template('verify_email.html', token=token)
            send_async_email(current_app._get_current_object(),[model.username], subject, body, html)
            #Thread(target=send_async_email, args=(current_app,msg)).start()
