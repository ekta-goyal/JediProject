from flask import request, redirect, url_for, jsonify, render_template, current_app, Blueprint, flash
from http import HTTPStatus
from flask_login import logout_user, login_user, login_required, current_user

from models import User, UserSchema, Team, TeamSchema, Task, TaskSchema
from marshmallow import INCLUDE
from app.database import db
from sqlalchemy import desc
from datetime import date
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
    except Exception as e:
        print(e)
        return 'error'

@api_blueprint.route('/accounts/login', methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username, type='regular-user').first()
    
    if user:
        if not user.is_verified:
            errors = {"error": "User Not Verified, Reregister from admin."}

        elif user.is_correct_password(password):
            login_user(user)
            data = get_data(user, UserSchema, request=request, many=False)
            if data != 'error':
                return jsonify(data), HTTPStatus.OK
            else:
                return '', HTTPStatus.BAD_REQUEST
        else:
            errors = {"error": "Password invalid"}
    else:
        errors = {"error": "Username invalid"}
    return jsonify(errors), HTTPStatus.UNAUTHORIZED


@api_blueprint.route('/accounts/logout', methods=['GET'])
def logout():
    logout_user()
    return '', HTTPStatus.NO_CONTENT

@api_blueprint.route('/accounts/forget', methods=['POST'])
def forget():
    from app.crypt import get_time_token
    from app.mail import send_async_email
    try:
        user_name = request.form['username']
        token = get_time_token(user_name, salt="forget-password")
        subject = "Forget Password"
        body = "This is body"
        html = f"""<!DOCTYPE html><html><body><a style='color="red"'>{token}</a></body></html>"""
        send_async_email(current_app._get_current_object(),[user_name], subject, body, html)
        return '', HTTPStatus.OK
    except:
        return '', HTTPStatus.BAD_REQUEST

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
    if data != 'error':
        return jsonify(data), HTTPStatus.OK
    else:
        return '', HTTPStatus.BAD_REQUEST

@api_blueprint.route('/teams', methods=['GET'])
@api_blueprint.route('/team/<int:id>', methods=['GET'])
@login_required
def get_team(id=None):
    if id:
        team = Team.query.filter_by(id=id).first_or_404()
        data = get_data(team, TeamSchema, request=request, many=False)
    else:
        teams = Team.query.all()
        data = get_data(teams, TeamSchema, request=request, many=True)
    if data != 'error':
        return jsonify(data), HTTPStatus.OK
    else:
        return '', HTTPStatus.BAD_REQUEST

@api_blueprint.route('/team/<int:team_id>/banner', methods=['GET'])
@login_required
def get_team_banner(team_id):
    rs = db.engine.execute(f'SELECT team_id,user_id,is_verified,color,image_index,image_link FROM User_Team_Mapping where user_id={current_user.id} AND team_id={team_id}')
    team_id,user_id,is_verified,color,image_index,image_link = [None]*6
    for x in rs:
        team_id,user_id,is_verified,color,image_index,image_link = x
        break
    return jsonify({
        "team_id": team_id,
        "user_id": user_id,
        "is_verified": is_verified,
        "color": color,
        "index": image_index,
        "link": image_link
    }), HTTPStatus.OK

@api_blueprint.route('/user/<int:user_id>/teams', methods=['GET'])
@login_required
def get_user_teams(user_id):
    user = User.query.filter_by(id=user_id, type='regular-user', is_verified=1).first_or_404()
    data = get_data(user.teams, TeamSchema, request=request, many=True)
    if data != 'error':
        return jsonify(data), HTTPStatus.OK
    else:
        return '', HTTPStatus.BAD_REQUEST

@api_blueprint.route('/team/<int:team_id>/users', methods=['GET'])
@login_required
def get_team_users(team_id):
    team = Team.query.filter_by(id=team_id).first_or_404()
    data = get_data(team.users, UserSchema, request=request, many=True)
    if data != 'error':
        return jsonify(data), HTTPStatus.OK
    else:
        return '', HTTPStatus.BAD_REQUEST

@api_blueprint.route('/team/<int:team_id>/tasks', methods=['GET'])
@login_required
def get_team_tasks(team_id):
    status = request.args.get('status', '')
    if status in ["my"]:
        id = current_user.get_id()
        tasks = Task.query.filter_by(assignee_id=id).join(Team).filter_by(id=team_id).order_by(desc(Task.expected_end_date)).all()
        data = get_data(tasks, TaskSchema, request=request, many=True)
    elif status:
        tasks = Task.query.filter_by(task_status=status).join(Team).filter_by(id=team_id).order_by(desc(Task.expected_end_date)).all()
        data = get_data(tasks, TaskSchema, request=request, many=True)
    else:
        team = Team.query.filter_by(id=team_id).first_or_404()
        data = get_data(team.tasks, TaskSchema, request=request, many=True)
    if data != 'error':
        return jsonify(data), HTTPStatus.OK
    else:
        return '', HTTPStatus.BAD_REQUEST


@api_blueprint.route('/tasks', methods=['GET'])
@login_required
def get_my_tasks():
    status = request.args.get('status', '')
    if status in ["end"]:
        id = current_user.get_id()
        tasks = Task.query.filter_by(assignee_id=id).filter(Task.expected_end_date >= date.today()).filter(Task.task_status != 'DONE').order_by(desc(Task.expected_end_date)).all()
        data = get_data(tasks, TaskSchema, request=request, many=True)
    elif status in ["start"]:
        id = current_user.get_id()
        tasks = Task.query.filter_by(assignee_id=id).filter(Task.start_date >= date.today()).filter(Task.task_status != 'DONE').order_by(desc(Task.start_date)).all()
        data = get_data(tasks, TaskSchema, request=request, many=True)
    else:
        data = 'error'
    if data != 'error':
        return jsonify(data), HTTPStatus.OK
    else:
        return '', HTTPStatus.BAD_REQUEST



@api_blueprint.route('/reporterTasks', methods=['GET'])
def reporter_tasks():
    userID = current_user.id
    tasks = Task.query.filter(Task.reporter_id==userID).order_by(desc(Task.created_at)).all()
    data = get_data(tasks, TaskSchema, request=request, many=True)
    return jsonify(data), HTTPStatus.OK

@api_blueprint.route('/myPerformance/<int:userID>', methods=['GET'])
def get_performance(userID):
    user = User.query.filter_by(id=userID).all()
    data = get_data(user, UserSchema, request=request, many=True)
    return jsonify(data), HTTPStatus.OK
