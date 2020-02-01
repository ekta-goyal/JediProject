from flask import request, redirect, url_for, jsonify, render_template, current_app, Blueprint
from http import HTTPStatus
from flask_login import logout_user, login_user
from app.workforceapp.models import User, UserSchema

regular_html_blueprint = Blueprint('regular_html_blueprint', __name__)
regular_api_blueprint = Blueprint('regular_api_blueprint', __name__)


@regular_api_blueprint.route('/accounts/login', methods=['POST'])
def admin_login():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username, password=password).first()
    schema = UserSchema().dump(user)
    try:
        login_user(user)
    except AttributeError:
        return jsonify(schema.data), HTTPStatus.UNAUTHORIZED
    else:
        return jsonify(schema.data), HTTPStatus.OK


@regular_api_blueprint.route('/accounts/logout', methods=['GET'])
def admin_logout():
    logout_user()
    return '', HTTPStatus.NO_CONTENT