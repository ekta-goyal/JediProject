from sqlalchemy.orm import relationship, backref
from app.database import db

UsersTeamMapping = db.Table("User_Team_Mapping",
    db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key = True),
    db.Column('team_id', db.Integer, db.ForeignKey('Team.id'), primary_key = True),
    db.Column('is_verified', db.Boolean, default=False),
    db.Column('color', db.String(7), default="#FFFFFF"),
    db.Column('image_index',db.Integer, default=0),
    db.Column('image_link',db.String(50), default='https://i.picsum.photos/id/0/5616/3744.jpg')
)
