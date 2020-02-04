from flask import request, redirect, url_for, jsonify, render_template, current_app, Blueprint, flash
from http import HTTPStatus
from flask_login import logout_user, login_user, login_required

from models import User, UserSchema, Team, TeamSchema, Task, TaskSchema
from marshmallow import INCLUDE
# from models import select

api_blueprint = Blueprint('api_blueprint', __name__)

def get_data(obj, schema, request=None, many=False):
    exclude = tuple(filter(None, request.args.get('exclude', '').split(',')))
    only = tuple(filter(None, request.args.get('only', '').split(',')))
    try:
        if exclude:
            data = schema(many=many, unknown=INCLUDE, exclude=exclude).dump(obj)
        elif only:
            data = schema(many=many, unknown=INCLUDE, only=only).dump(obj)
        else:
            data = schema(many=many, unknown=INCLUDE).dump(obj)
        return data
    except:
        return ''


@api_blueprint.route('/accounts/login', methods=['POST'])
def admin_login():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username, type='regular-user', is_verified=1).first()
    
    if user:
        if user.is_correct_password(password):
            login_user(user)
            data = get_data(user, UserSchema, request=request, many=False)
            if data:
                return jsonify(data), HTTPStatus.OK
            else:
                return '', HTTPStatus.BAD_REQUEST
        errors = {"error": "Password invalid"}
    else:
        errors = {"error": "Username invalid"}
    return jsonify(errors), HTTPStatus.UNAUTHORIZED


@api_blueprint.route('/accounts/logout', methods=['GET'])
def admin_logout():
    logout_user()
    return '', HTTPStatus.NO_CONTENT



@api_blueprint.route('/users', methods=['GET'])
@api_blueprint.route('/user/<int:id>', methods=['GET'])
@login_required
def get_user(id=None):
    if id:
        user = User.query.filter_by(id=id, type='regular-user', is_verified=1).first_or_404()
        data = get_data(user, UserSchema, request=request, many=False)
    else:
        users = User.query.filter_by(type='regular-user', is_verified=1).all()
        data = get_data(users, UserSchema, request=request, many=True)
    if data:
        return jsonify(data), HTTPStatus.OK
    else:
        return '', HTTPStatus.BAD_REQUEST

@api_blueprint.route('/teams/', methods=['GET'])
@api_blueprint.route('/team/<int:id>', methods=['GET'])
@login_required
def get_team(id=None):
    if id:
        team = Team.query.filter_by(id=id).first_or_404()
        data = get_data(team, TeamSchema, request=request, many=False)
    else:
        teams = Team.query.all()
        data = get_data(teams, TeamSchema, request=request, many=True)
    if data:
        return jsonify(data), HTTPStatus.OK
    else:
        return '', HTTPStatus.BAD_REQUEST


@api_blueprint.route('/user/<int:user_id>/teams/', methods=['GET'])
@login_required
def get_user_teams(user_id):
    user = User.query.filter_by(id=user_id, type='regular-user', is_verified=1).first_or_404()
    data = get_data(user.teams, TeamSchema, request=request, many=True)
    if data:
        return jsonify(data), HTTPStatus.OK
    else:
        return '', HTTPStatus.BAD_REQUEST

@api_blueprint.route('/team/<int:team_id>/users/', methods=['GET'])
@login_required
def get_team_users(team_id):
    team = Team.query.filter_by(id=team_id).first_or_404()
    data = get_data(team.users, UserSchema, request=request, many=True)
    if data:
        return jsonify(data), HTTPStatus.OK
    else:
        return '', HTTPStatus.BAD_REQUEST

@api_blueprint.route('/team/<int:team_id>/tasks/', methods=['GET'])
@login_required
def get_team_tasks(team_id):
    team = Team.query.filter_by(id=team_id).first_or_404()
    data = get_data(team.tasks, TaskSchema, request=request, many=True)
    if data:
        return jsonify(data), HTTPStatus.OK
    else:
        return '', HTTPStatus.BAD_REQUEST
