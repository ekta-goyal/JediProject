from flask_login import UserMixin
from sqlalchemy_utils import ChoiceType

from app.database import db, event
from app.loginmanager import login_manager
from app.workforceapp.models import base
from marshmallow import Schema, fields

class User(db.Model,base.Base,UserMixin):
    __tablename__ = 'User'
    USER_TYPES = [
        (u'admin', (u'Admin')),
        (u'regular-user', (u'Regular user'))
    ]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False,
                         index=True
                         )
    
    # password = db.Column(
    #     PasswordType(
    #         # The returned dictionary is forwarded to the CryptContext
    #         onload=lambda **kwargs: dict(
    #             schemes=flask.current_app.config['PASSWORD_SCHEMES'],
    #             **kwargs
    #         ),
    #     ),
    #     unique=False,
    #     nullable=False,
    # )
    password = db.Column(db.String(128))
    type = db.Column(ChoiceType(USER_TYPES, impl=db.String(12)), default='regular-user')
    # type = db.Column(db.String(100))
    is_verified = db.Column(db.Integer,default=0)
    contact = db.Column(db.String(20))


@event.listens_for(User.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    print("Adding Default values")
    db.session.add(User(
        name='Nitheesh Chandra',
        username="Nitheesh",
        password="nith@123",
        type='admin'
    ))
    db.session.add(User(
        name='Vishaka Shah',
        username="Vishaka",
        password="vish@123",
        type='admin'
    ))
    db.session.add(User(
        name='Ekta Goyal',
        username="Ekta",
        password="ekta@123",
        type='admin'
    ))
    db.session.commit()
    print("Added default values")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    username = fields.Email()
    is_verified = fields.Integer()
    created_at = fields.DateTime()
    modified = fields.DateTime()

    