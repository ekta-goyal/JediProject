from sqlalchemy.orm import relationship, backref
from app.workforceapp.models import base
from app.database import db


class User_team_mapping(db.Model,base.Base):
    __tablename__ = "User_team_mapping"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    team_color = db.Column(db.String(100))
    is_verified = db.Column(db.Integer, default=0)
    team_id = db.Column(db.Integer, db.ForeignKey('Team.id'))
    User = relationship("User", backref=backref("User", uselist=False))
    Team = relationship("Team", backref=backref("Team", uselist=False))

    def __init__(self,user_id,team_color,is_verified,team_id, User,Team):
        self.user_id = user_id
        self.team_color = team_color
        self.is_verified = is_verified
        self.team_id = team_id
        self.User = User
        self.Team = Team
