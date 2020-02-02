from flask_login import UserMixin
from sqlalchemy_utils import ChoiceType
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from app.database import db, event
from app.loginmanager import login_manager
from app.workforceapp.models import base
from app.crypt import bcrypt

from marshmallow import Schema, fields, post_load, validates, ValidationError

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
    _password = db.Column(db.Binary(60))
    type = db.Column(ChoiceType(USER_TYPES, impl=db.String(12)), default='regular-user')
    # type = db.Column(db.String(100))
    is_verified = db.Column(db.Integer,default=0)
    contact = db.Column(db.String(20))


    def __init__(self, **kwargs):
        self.password = str(kwargs["password"])
        del kwargs["password"]
        super(User, self).__init__(**kwargs)
    
    @hybrid_property
    def password(self):
        return self._password
 
    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password)
 
    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)


@event.listens_for(User.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    print("Adding Default values")
    db.session.add_all([
        User(
            name='Nitheesh Chandra',
            username="Nitheesh",
            password="nith@123",
            type='admin'
        ),
        User(
            name='Vishaka Shah',
            username="Vishaka",
            password="vish@123",
            type='admin'
        ),
        User(
            name='Ekta Goyal',
            username="Ekta",
            password="ekta@123",
            type='admin'
        )
    ])
    print("Added admins, now test users...")
    db.session.add_all([
        User(
            name='User1',
            username="user1@test.com",
            password="password",
            type='regular-user',
            is_verified=1
        ),
        User(
            name='User2',
            username="user2@test.com",
            password="password",
            type='regular-user',
            is_verified=1
        ),
        User(
            name='User3',
            username="user3@test.com",
            password="password",
            type='regular-user',
            is_verified=0
        )
    ])
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

    uri = fields.Method("get_item_uri")
    
    def get_item_uri(self, obj):

        return f'/api/v1/user/{obj.id}/'

if __name__ == '__main__':
    print("In user madel")