from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms import TextAreaField
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from wtforms_alchemy import QuerySelectField
from models import User, Team
from wtforms import MultipleFileField


class AddTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators = [DataRequired()])
    expected_end_date = DateField('Expected End Date',validators=[DataRequired()])
    priority = StringField('Priority', validators=[DataRequired()])
    assignee = QuerySelectField(
        query_factory=lambda: User.query.all(),
        get_pk=lambda a: a.id,
        get_label=lambda a: a.name,
        allow_blank=False,
    )
    team = QuerySelectField(
        query_factory=lambda: Team.query.all(),
        get_pk=lambda a: a.id,
        get_label=lambda a: a.name,
        allow_blank=False,
    )
    attachments = MultipleFileField('Upload Attachments')
    submit = SubmitField('Create Task')