from flask import request, redirect, url_for, render_template, Blueprint
from itsdangerous import SignatureExpired, BadTimeSignature
from http import HTTPStatus
from flask_login import login_required,current_user

html_blueprint = Blueprint('html_blueprint', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='web/static'
    )

@html_blueprint.route('/', methods=['GET'])
def index():
    return render_template('login.html')
    
@html_blueprint.route('/dashboard', methods=['GET'])
@login_required
def home():
    user = current_user
    if user:
        return render_template('home.html',user=user)
    else:
        return '', HTTPStatus.BAD_REQUEST

@html_blueprint.route('/debug-sentry')
def trigger_error():
    try:
        division_by_zero = 1 / 0
    except:
        print("Error")