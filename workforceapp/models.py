import flask

from app import app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from flask_marshmallow import Marshmallow
import os
from flask_migrate import Migrate,MigrateCommand
from sqlalchemy.sql import func
from sqlalchemy_utils import  force_auto_coercion, ChoiceType  # Password data type

# import enum #for choice data type
# force_auto_coercion()

db = SQLAlchemy(app)

ma = Marshmallow(app)
#Creating a migrate object
migrate = Migrate(app, db)

#
# class UserType(enum.Enum):
#     admin = 1
#     regular = 2
#
class Base:
    deleted_at = db.Column(db.DateTime,default=None)
    created_at = db.Column(db.DateTime,server_default= func.now())
    modified = db.Column(db.DateTime,onupdate=func.now())

class User(db.Model,Base):

    __tablename__ = 'User'
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
    # type = db.Column(ChoiceType(UserType))
    type = db.Column(db.String(100))
    is_verified = db.Column(db.Integer,default=0)
    contact = db.Column(db.String(20))

    def __init__(self, name, password, type,is_verified,contact):
        self.name = name
        self.password = password
        self.type = type
        self.is_verified = is_verified
        self.contact = contact

class Team(db.Model,Base):
    __tablename__ = "Team"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))

    def __init__(self, name, description):
        self.name = name
        self.description = description

class User_team_mapping(db.Model,Base):
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

class Task_status(db.Model,Base):
    __tablename__ = "Task_status"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

# class Priority(enum.Enum):
#     major = 1
#     normal = 2
#     minor = 3

class BaseTask(Base):
    modified_by = db.Column(db.String(100))
    deleted_by = db.Column(db.String(100))

class Task(db.Model,BaseTask):
    __tablename__ = "Task"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    start_date = db.Column(db.Date(),nullable=False)
    expected_end_date = db.Column(db.Date(),nullable=True)
    actual_end_date = db.Column(db.Date(),nullable=True)
    status = db.Column(db.Integer, db.ForeignKey('Task_status.id'))
    Task_status = relationship("Task_status", backref=backref("Task_status", uselist=False))
    priority = db.Column(db.String(100))

    reporter = db.Column(db.Integer, db.ForeignKey("User.id"))
    assignee = db.Column(db.Integer, db.ForeignKey('User.id'))

    User = relationship(
        'User',
        primaryjoin=(
            'and_('
            'Task.reporter == User.id, '
            'Task.assignee == User.id'
            ')'
        ),
        innerjoin=True
    )

    # User_reporter = relationship("User", backref="User_reporter", foreign_keys="User.reporter")
    # User_assignee = relationship("User", backref="User_assigned", foreign_keys="User.assignee")
    def __init__(self,title,description,start_date,expected_end_date,actual_end_date,status,priority,reporter,assignee):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.expected_end_date = expected_end_date
        self.actual_end_date = actual_end_date
        self.status = status
        self.priority = priority
        self.reporter = reporter
        self.assignee = assignee

class Task_index_mapping(db.Model,Base):
    id = db.Column(db.Integer,primary_key=True)
    task_index = db.Column(db.Integer)
    task_id = db.Column(db.Integer,db.ForeignKey('Task.id'))

    Task = relationship("Task", backref=backref("Task", uselist=False))

    def __init__(self,task_index,task_id):
        self.task_index = task_index
        self.task_id = task_id

class Attachments(db.Model,Base):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    path = db.Column(db.String(200))
    task_id = db.Column(db.Integer, db.ForeignKey('Task.id'))

    Task = relationship("Task", backref=backref("Task_Attachments", uselist=False))

    def __init__(self,name,path,task_id):
        self.name = name
        self.path = path
        self.task_id = task_id

class Assignee_report(db.Model,Base):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    assignee_performance = db.Column(db.String(100))

    User = relationship("User", backref=backref("User_Assignee_report", uselist=False))

    def __init__(self,user_id,assignee_performance):
        self.user_id = user_id
        self.assignee_performance = assignee_performance









