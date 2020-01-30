from app.workforceapp.models import base

from app.database import db
from sqlalchemy.orm import relationship, backref


class Attachments(db.Model,base.Base):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    path = db.Column(db.String(200))
    task_id = db.Column(db.Integer, db.ForeignKey('Task.id'))

    Task = relationship("Task", backref=backref("Task_Attachments", uselist=False))

    def __init__(self,name,path,task_id):
        self.name = name
        self.path = path
        self.task_id = task_id
