from flask_login import UserMixin
from sqlalchemy_utils import ChoiceType
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from app.database import db
from app.loginmanager import login_manager
from .utils import At
from app.crypt import bcrypt
from . import UsersTeamMapping
from marshmallow import Schema, fields, post_load, validates, ValidationError
from flask import redirect, request, url_for

class User(db.Model, UserMixin, At):
    __tablename__ = 'User'
    USER_TYPES = [
        (u'admin', (u'Admin')),
        (u'regular-user', (u'Regular user'))
    ]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    _password = db.Column(db.Binary(60), name = "password")
    type = db.Column(ChoiceType(USER_TYPES, impl=db.String(12)), default='regular-user')
    designation = db.Column(db.String(100))
    is_verified = db.Column(db.Boolean,default=False)
    contact = db.Column(db.String(20))

    teams = db.relationship('Team', secondary=UsersTeamMapping, backref=db.backref('members', lazy='dynamic'))


    def __init__(self, **kwargs):
        self.password = str(kwargs["password"])
        del kwargs["password"]
        super(User, self).__init__(**kwargs)
    
    def __str__(self):
        return f"{self.name}, {self.username}"

    @hybrid_property
    def password(self):
        return self._password
 
    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password)
 
    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('html_blueprint.index', next = request.path))

class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    username = fields.Email()
    is_verified = fields.Boolean()
    created_at = fields.DateTime()
    modified_at = fields.DateTime()
    contact = fields.String()
    designation = fields.String()

    teams = fields.List(fields.Nested("TeamSchema",exclude=("members",)))

    uri = fields.Method("get_item_uri")
    
    teams_count = fields.Method("get_len_teams")

    performance = fields.Method("get_performance")
    
    def get_item_uri(self, obj):
        return f'/api/v1/user/{obj.id}/'

    def get_len_teams(self, obj):
        return len(obj.teams)

    def get_performance(self, obj):
        tasks = obj.as_assignee
        print(type(tasks))
        total_cnt = len(tasks)
        print("--------------------------- " + str(total_cnt))
        cnt = 0
        percentage = 0
        if total_cnt > 0:
            for eachtask in tasks:
                print(eachtask.actual_end_date)
                print(eachtask.title)
                if eachtask.actual_end_date != None:
                    print("-----inside-----")
                    if eachtask.expected_end_date <= eachtask.actual_end_date:
                        cnt = cnt + 1
            percentage = (cnt * 100) / total_cnt
        print(percentage, total_cnt, cnt)
        return percentage


if __name__ == '__main__':
    print("In user madel")