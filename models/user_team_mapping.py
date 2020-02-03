from sqlalchemy.orm import relationship, backref
from app.database import db

UsersTeamMapping = db.Table("User_Team_Mapping",
    db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('Team.id')),
    # db.Column('is_verified', db.Integer, default=0),
    # db.Column('color', db.String(7))
)
