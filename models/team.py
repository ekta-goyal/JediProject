from .utils import At
from app.database import db

from marshmallow import Schema, fields, post_load, validates, ValidationError

class Team(db.Model,At):
    __tablename__ = "Team"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)

class TeamSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    created_at = fields.DateTime()
    modified = fields.DateTime()
    
    uri = fields.Method("get_item_uri")

    members = fields.List(fields.Nested("UserSchema",exclude=("teams",)))
    
    def get_item_uri(self, obj):
        return f'/api/v1/team/{obj.id}/'
