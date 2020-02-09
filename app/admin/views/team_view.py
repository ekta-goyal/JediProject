from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, current_app, render_template
from flask_login import current_user
from wtforms.validators import DataRequired
from app.mail import send_async_email
from flask_mail import Message

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


    can_create = True
    can_delete = True
    can_edit = True

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
            subject = "Invitation | Added To a Team | Work Together. Starts Here"
            from app.crypt import get_time_token
            for member in model.members:
                token = get_time_token(f"{model.id},{member.id}", salt="team-user")
                body = token
                html = render_template('team_invite.html', token=token, team = model.name)
                send_async_email(current_app._get_current_object(),[member.username], subject, body, html)
            #Thread(target=send_async_email, args=(current_app,msg)).start()
