from flask_login import UserMixin
from sqlalchemy_utils import ChoiceType

from app.database import db
from app.loginmanager import login_manager
from app.workforceapp.models import base

class User(db.Model,base.Base,UserMixin):
    __tablename__ = 'User'
    USER_TYPES = [
        (u'admin', (u'Admin')),
        (u'regular-user', (u'Regular user'))
    ]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
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
    password = db.Column(db.String(100))
    type = db.Column(ChoiceType(USER_TYPES))
    # type = db.Column(db.String(100))
    is_verified = db.Column(db.Integer,default=0)
    contact = db.Column(db.String(20))


    def __init__(self, name, password, type,is_verified,contact):
        self.name = name
        self.password = password
        self.type = type
        self.is_verified = is_verified
        self.contact = contact


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)







