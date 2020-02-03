from app.database import db

class By:
    modified_by = db.Column(db.String(100))
    deleted_by = db.Column(db.String(100))
