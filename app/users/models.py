from datetime import datetime

from app.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=20), unique=True, nullable=False,
                         index=True
                         )
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    emails = db.relationship(
        "UserEmail",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "order_by": created_at
    }
    __tablename__ = 'user'

    def __repr__(self):
        return (
            '<{class_name}('
            'user_id={self.id}, '
            'username="{self.username}")>'.format(
                class_name=self.__class__.__name__,
                self=self
            )
        )


class UserEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    email = db.Column(db.String(120), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    __mapper_args__ = {
        "order_by": created_at
    }
    __tablename__ = 'user_email'

    def __repr__(self):
        return (
            '<{class_name}('
            'user_id={self.id}, '
            'username="{self.user.username}")'
            'email="{self.email}">'.format(
                class_name=self.__class__.__name__,
                self=self
            )
        )
