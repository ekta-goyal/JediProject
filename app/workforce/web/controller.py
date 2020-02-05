from flask import request, redirect, url_for, render_template, Blueprint
from http import HTTPStatus

html_blueprint = Blueprint('html_blueprint', __name__, template_folder='templates')

@html_blueprint.route('/', methods=['GET'])
def index():
    user = {'username': 'Nitheesh'}
    return render_template('home.html', title='Home', user=user)