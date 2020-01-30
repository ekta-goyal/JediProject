from sqlalchemy.orm import relationship, backref

from app.workforceapp.models import base

from app.database import db


class Task_index_mapping(db.Model,base.Base):
    id = db.Column(db.Integer,primary_key=True)
    task_index = db.Column(db.Integer)
    task_id = db.Column(db.Integer,db.ForeignKey('Task.id'))

    Task = relationship("Task", backref=backref("Task", uselist=False))

    def __init__(self,task_index,task_id):
        self.task_index = task_index
        self.task_id = task_id
