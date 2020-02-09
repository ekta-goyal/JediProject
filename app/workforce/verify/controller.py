from flask import request, redirect, url_for, render_template, Blueprint
from itsdangerous import SignatureExpired, BadTimeSignature
from http import HTTPStatus
from models import User
from app.database import db

verify_blueprint = Blueprint('verify_blueprint', __name__, template_folder='templates')

@verify_blueprint.route('/user/<token>', methods=['GET', 'POST'])
def confirm_email(token): 
    from app.crypt import get_token_data
    if request.method == 'POST':
        password = request.form["password"]
        designation = request.form["designation"]
        contact = request.form["contact"]
        token = request.form["token"]
        mail_id = get_token_data(token, salt="user-create", max_age=1*24*60*60)
        user = User.query.filter_by(username=mail_id).first_or_404()
        user.is_verified = True
        user.password = password
        user.designation = designation
        user.contact = contact
        db.commit()
        return redirect(url_for('html_blueprint.index'))
    else:
        try:
            email = get_token_data(token, salt="user-create", max_age=1*24*60*60)
            user = User.query.filter_by(username=email).first()
            return render_template('new_user.html',user=user, token=token)
        except SignatureExpired:
            return 'Token Expired'
        except BadTimeSignature:
            return 'Invalid Token'
        return f'Tokens Works {email}'

@verify_blueprint.route('/team/<token>')
def confirm_team(token): 
    from app.crypt import get_token_data
    try:
        payload = get_token_data(token, salt="team-user", max_age=3600)
        team_id, user_id = payload.split(',')
        team_id, user_id = int(team_id), int(user_id)
        db.engine.execute(f'UPDATE User_Team_Mapping SET is_verified = true WHERE team_id = {team_id} AND user_id = {user_id}')
    except SignatureExpired:
        return 'Token Expired'
    except BadTimeSignature:
        return 'Invalid Token'
    return f'Tokens Works'

@verify_blueprint.route('/forget/<token>', methods =['GET', 'POST'])
def forget_pass(token): 
    from app.crypt import get_token_data
    if request.method == 'POST':
        password = request.form["password"]
        token = request.form["token"]
        mail_id = get_token_data(token, salt="forget-password", max_age=3600)
        user = User.query.filter_by(username=mail_id, type='regular-user').first_or_404()
        user.is_verified = True
        user.password = password
        db.commit()
        return redirect(url_for('html_blueprint.index'))
    else:
        try:
            mail_id = get_token_data(token, salt="forget-password", max_age=3600)
            return render_template('reset_pass.html',token=token, mail_id=mail_id)
        except SignatureExpired:
            return 'Token Expired'
        except BadTimeSignature:
            return 'Invalid Token'
        return f'Tokens Works'

