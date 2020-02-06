from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, current_app
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
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):    
        return redirect(url_for('admin_html_blueprint.admin_login'))

    def after_model_change(self, form, model, is_created):
        if is_created:
            subject = "New Team"
            body = "This is body"
            from app.crypt import get_time_token
            for member in model.members:
                token = get_time_token(f"{model.id},{member.id}", salt="team-user")
                html = f"""<!DOCTYPE html><html><body><a style='color="red"'>{token}</a></body></html>"""
                send_async_email(current_app._get_current_object(),[member.username], subject, body, html)
            #Thread(target=send_async_email, args=(current_app,msg)).start()
