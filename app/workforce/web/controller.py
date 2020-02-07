from flask import request, redirect, url_for, render_template, Blueprint
from itsdangerous import SignatureExpired, BadTimeSignature
from http import HTTPStatus

html_blueprint = Blueprint('html_blueprint', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='web/static'
    )

@html_blueprint.route('/', methods=['GET'])
def index():
    user = {'username': 'Nitheesh'}
    return render_template('main.html', title='Home', user=user)

@html_blueprint.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0