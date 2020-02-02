from app.workforceapp.models import base
from app.database import db, event

from marshmallow import Schema, fields, post_load, validates, ValidationError

class Team(db.Model,base.Base):
    __tablename__ = "Team"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))


@event.listens_for(Team.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    print("Adding Default values")
    db.session.add_all([
        Team(
            name='Team1',
            description='''# Team1
This a sample team, used to follow:
- time
- coffee
- fun
            '''
        ),
        Team(
            name='Team2',
            description='''# Team1
This a sample team, used to follow:
- sleep
- work
- learn '''
        ),
        Team(
            name='Team1',
            description='''# Team3
This a sample team, used to follow:
- cool
- bisket
- cake '''
            )
    ])
    db.session.commit()
    print("Added default values")


class TeamSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    created_at = fields.DateTime()
    modified = fields.DateTime()
    
    uri = fields.Method("get_item_uri")
    
    def get_item_uri(self, obj):
        return f'/api/v1/team/{obj.id}/'
