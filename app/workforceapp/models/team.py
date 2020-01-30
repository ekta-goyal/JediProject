from app.workforceapp.models import base
from app.database import db


class Team(db.Model,base.Base):
    __tablename__ = "Team"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))

    def __init__(self, name, description):
        self.name = name
        self.description = description
