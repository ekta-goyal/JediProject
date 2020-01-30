from sqlalchemy.orm import relationship, backref

from app.workforceapp.models import base

from app.database import db

class Assignee_report(db.Model,base.Base):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    assignee_performance = db.Column(db.String(100))

    User = relationship("User", backref=backref("User_Assignee_report", uselist=False))

    def __init__(self,user_id,assignee_performance):
        self.user_id = user_id
        self.assignee_performance = assignee_performance

