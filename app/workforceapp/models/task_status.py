from app.workforceapp.models import base
from app.database import db


class Task_status(db.Model,base.Base):
    __tablename__ = "Task_status"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name
