
import flask


from app.database import db
from flask import Flask

from sqlalchemy.orm import relationship, backref

import os
from sqlalchemy.sql import func
from sqlalchemy_utils import  force_auto_coercion, ChoiceType  # Password data type
from flask_login import UserMixin

class Base:
    deleted_at = db.Column(db.DateTime,default=None)
    created_at = db.Column(db.DateTime,server_default=func.now())
    modified = db.Column(db.DateTime,onupdate=func.now())
