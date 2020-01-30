from sqlalchemy_utils import ChoiceType

from app.workforceapp.models import base_task

from app.database import db
from sqlalchemy.orm import relationship, backref

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

    # User_reporter = relationship("User", backref="User_reporter", foreign_keys="User.reporter")
    # User_assignee = relationship("User", backref="User_assigned", foreign_keys="User.assignee")
    def __init__(self,title,description,start_date,expected_end_date,actual_end_date,status,priority,reporter,assignee):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.expected_end_date = expected_end_date
        self.actual_end_date = actual_end_date
        self.status = status
        self.priority = priority
        self.reporter = reporter
        self.assignee = assignee
