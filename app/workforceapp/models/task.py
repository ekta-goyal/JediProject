from sqlalchemy_utils import ChoiceType

from app.workforceapp.models import base_task

from app.database import db
from sqlalchemy.orm import relationship, backref
from marshmallow import Schema, fields, post_load, validates, ValidationError

class Task(db.Model,base_task.BaseTask):
    __tablename__ = "Task"
    Priority = [
        ('major','major'),
        ('normal','normal'),
        ('minor','minor')
    ]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    start_date = db.Column(db.Date(),nullable=False)
    expected_end_date = db.Column(db.Date(),nullable=True)
    actual_end_date = db.Column(db.Date(),nullable=True)
    status = db.Column(db.Integer, db.ForeignKey('Task_status.id'))
    Task_status = relationship("Task_status", backref=backref("Task_status", uselist=False))
    priority = db.Column(ChoiceType(Priority))

    reporter = db.Column(db.Integer, db.ForeignKey("User.id"))
    assignee = db.Column(db.Integer, db.ForeignKey('User.id'))

    User = relationship(
        'User',
        primaryjoin=(
            'and_('
            'Task.reporter == User.id, '
            'Task.assignee == User.id'
            ')'
        ),
        innerjoin=True
    )


class TaskSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    created_at = fields.DateTime()
    modified = fields.DateTime()
    
    uri = fields.Method("get_item_uri")
    
    def get_item_uri(self, obj):
        return f'/api/v1/team/{obj.id}/'
