from app.database import db
from sqlalchemy.sql import func

class At:
    deleted_at = db.Column(db.DateTime,default=None)
    created_at = db.Column(db.DateTime,server_default=func.now())
    modified_at = db.Column(db.DateTime,onupdate=func.now())
