from app.workforceapp.models import base

from app.database import db

class BaseTask(base.Base):
    modified_by = db.Column(db.String(100))
    deleted_by = db.Column(db.String(100))
