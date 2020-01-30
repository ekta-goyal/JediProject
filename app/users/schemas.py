from marshmallow import Schema, fields, post_load, validates, ValidationError

from app.database import db
from app.users.models import User, UserEmail


class UserEmailSchema(Schema):
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    emails = fields.Nested(UserEmailSchema, many=True, required=True)
    created_at = fields.DateTime(dump_only=True)
    uri = fields.Method("get_item_uri")

    def get_item_uri(self, obj):
        return '/api/v1/users/{obj.username}/'.format(
            obj=obj,
        )

    @validates('username')
    def validate_username(self, username, **kwargs):
        if bool(User.query.filter_by(username=username).first()):
            raise ValidationError(
                '"{username}" username already exists, '
                'please use a different username.'.format(username=username)
            )

    @validates('emails')
    def validate_emails(self, emails):
        exists_in_user_emails = []
        for d in emails:
            email = d.get('email')
            if bool(UserEmail.query.filter_by(email=email).first()):
                exists_in_user_emails.append(email)

        if exists_in_user_emails:
            raise ValidationError(
                '"{emails}" emails already exists, '
                'please try different emails.'.format(
                    emails=", ".join(exists_in_user_emails)
                )
            )

    @post_load
    def create_user(self, data):
        email_list = data.pop('emails', list())
        user = User(**data)
        user_emails = [UserEmail(email=d.get('email')) for d in email_list]
        user.emails.extend(user_emails)
        db.session.add(user)
        db.session.add_all(user_emails)
        db.session.commit()
        self.instance = user

    def update_user(self, user, data):
        user.username = data.get('username', user.username)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        emails = data.get('emails')
        if emails:
            UserEmail.query.filter_by(user_id=user.id).delete()
            db.session.commit()
            new_user_emails = [UserEmail(email=d.get('email')) for d in emails]
            user.emails.extend(new_user_emails)
            db.session.add_all(new_user_emails)
        db.session.commit()
