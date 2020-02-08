from .utils import At, By
from app.database import db

from marshmallow import Schema, fields, post_load, validates, ValidationError
from sqlalchemy_utils import ChoiceType

class Attachments(db.Model, At, By):
    __tablename__ = "Attachments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    path = db.Column(db.String(100))
    task_id = db.Column(db.Integer, db.ForeignKey('Task.id'))
    task = db.relationship('Task', backref=db.backref('attachments', lazy='dynamic'))

class AttachmentSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    path = fields.String()


