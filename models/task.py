from .utils import At, By
from app.database import db

from marshmallow import Schema, fields, post_load, validates, ValidationError
from sqlalchemy_utils import ChoiceType

class Task(db.Model, At, By):
    __tablename__ = "Task"
    PRIORITY_VALUES = [
        ('low','low'),
        ('medium','medium'),
        ('high','high')
    ]
    STATUS_VALUES = [
        ('TODO','TODO'),
        ('DOING','DOING'),
        ('DONE','DONE')
    ]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    start_date = db.Column(db.Date(), nullable=False)
    expected_end_date = db.Column(db.Date(),nullable=True)
    actual_end_date = db.Column(db.Date())
    task_status = db.Column(ChoiceType(STATUS_VALUES, impl=db.String(5)), default='TODO', nullable=True)
    priority = db.Column(ChoiceType(PRIORITY_VALUES, impl=db.String(7)), default='medium')

    reporter_id = db.Column(db.Integer,db.ForeignKey('User.id'))
    assignee_id = db.Column(db.Integer,db.ForeignKey('User.id'))
    team_id = db.Column(db.Integer,db.ForeignKey('Team.id'))

    reporter = db.relationship('User', backref=db.backref('as_reporter', lazy='dynamic'), primaryjoin="User.id==Task.reporter_id")
    assignee = db.relationship('User', backref=db.backref('as_assignee', lazy='dynamic'), primaryjoin="User.id==Task.assignee_id")

    team = db.relationship('Team', backref=db.backref('tasks', lazy='dynamic'))

class TaskSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    start_date = fields.Date()
    expected_end_date = fields.Date()
    actual_end_date = fields.Date()
    task_status = fields.Method("get_status")
    priority = fields.Method("get_priority")
    reporter = fields.Nested("UserSchema",exclude=("teams","teams_count"))
    assignee = fields.Nested("UserSchema",exclude=("teams","teams_count"))
    team = fields.Nested("TeamSchema", exclude=("members","tasks"))
    attachments = fields.Nested("AttachmentSchema")
    created_at = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    modified_by = fields.String()
    modified_at = fields.DateTime()
    deleted_by = fields.String()
    deleted_at = fields.DateTime()
    assignee_name = fields.Method("get_assignee_name")
    reporter_name = fields.Method("get_reporter_name")

    def get_priority(self, obj):
        return obj.priority.code

    def get_status(self, obj):
        return obj.task_status.code

    def get_assignee_name(self, obj):
        return obj.assignee.name
    def get_reporter_name(self, obj):
        return obj.assignee.name