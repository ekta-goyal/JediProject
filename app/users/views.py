from http import HTTPStatus

from flask import Blueprint, jsonify
from flask import request

from app.users.models import User
from app.users.schemas import UserSchema
from app.database import db

users_api = Blueprint('users_api', __name__)


@users_api.route('/', methods=["GET"])
@users_api.route('/<string:username>/', methods=["GET"])
def retrieve_users(username=None):
    if username:
        user = User.query.filter_by(username=username).first_or_404()
        schema = UserSchema().dump(user)
        return jsonify(schema.data), HTTPStatus.OK

    users = User.query.all()
    schema = UserSchema(many=True).dump(users)
    return jsonify(schema.data), HTTPStatus.OK


@users_api.route('/', methods=["POST"])
def create_user():
    data = request.form
    schema = UserSchema()
    print(data)
    validated_data, errors = schema.load(data)

    if errors:
        return jsonify([errors, validated_data, data]), HTTPStatus.BAD_REQUEST
    return jsonify(schema.dump(schema.instance).data), HTTPStatus.CREATED


@users_api.route('/<string:username>/', methods=["PUT", "PATCH"])
def update_user(username):
    user = User.query.filter_by(username=username).first_or_404()

    data = request.get_json()

    schema = UserSchema()
    if request.method == 'PATCH':
        errors = schema.validate(data, partial=True)
    else:
        errors = schema.validate(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    schema.update_user(user, data)
    updated_user = User.query.filter_by(id=user.id).first()
    return jsonify(UserSchema().dump(updated_user).data), HTTPStatus.ACCEPTED


@users_api.route('/<string:username>/', methods=["DELETE"])
def delete_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return '', HTTPStatus.NO_CONTENT
