from flask import request, redirect, url_for, jsonify, render_template, current_app, Blueprint, flash
from http import HTTPStatus
from flask_login import logout_user, login_user, login_required

from models import User, UserSchema, Team, TeamSchema

api_blueprint = Blueprint('api_blueprint', __name__)

@api_blueprint.route('/accounts/login', methods=['POST'])
def admin_login():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username, type='regular-user', is_verified=1).first()
    
    if user:
        if user.is_correct_password(password):
            login_user(user)
            data = UserSchema().dump(user)
            return jsonify(data), HTTPStatus.OK
        errors = {"error": "Password invalid"}
    else:
        errors = {"error": "Username invalid"}
    return jsonify(errors), HTTPStatus.UNAUTHORIZED


@api_blueprint.route('/accounts/logout', methods=['GET'])
def admin_logout():
    logout_user()
    return '', HTTPStatus.NO_CONTENT



@api_blueprint.route('/users/', methods=['GET'])
@api_blueprint.route('/user/<int:id>', methods=['GET'])
@login_required
def get_user(id=None):
    if id:
        user = User.query.filter_by(id=id, type='regular-user', is_verified=1).first_or_404()
        data = UserSchema().dump(user)
    else:
        users = User.query.filter_by(type='regular-user', is_verified=1).all()
        data = UserSchema(many=True).dump(users)
    return jsonify(data), HTTPStatus.OK

@api_blueprint.route('/teams/', methods=['GET'])
@api_blueprint.route('/team/<int:id>', methods=['GET'])
@login_required
def get_team(id=None):
    if id:
        team = Team.query.filter_by(id=id).first_or_404()
        data = TeamSchema().dump(team)
    else:
        teams = Team.query.all()
        data = TeamSchema(many=True).dump(teams)
    return jsonify(data), HTTPStatus.OK


@api_blueprint.route('/user/<int:user_id>/teams/', methods=['GET'])
@login_required
def get_user_teams(user_id=None):
    if user_id:
        user = User.query.filter_by(id=user_id, type='regular-user', is_verified=1).first_or_404()
        data = TeamSchema(many=True).dump(user.teams)
        return jsonify(data), HTTPStatus.OK
    else:
        return '', HTTPStatus.BAD_REQUEST