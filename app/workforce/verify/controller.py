from flask import request, redirect, url_for, render_template, Blueprint
from itsdangerous import SignatureExpired, BadTimeSignature
from http import HTTPStatus
from models import User
from app.database import db
from flask_login import logout_user

verify_blueprint = Blueprint('verify_blueprint', __name__, template_folder='templates')

@verify_blueprint.route('/user/<token>', methods=['GET', 'POST'])
def confirm_email(token): 
    from app.crypt import get_token_data
    if request.method == 'POST':
        password = request.form["password"]
        designation = request.form["designation"]
        contact = request.form["contact"]
        mail_id = get_token_data(token, salt="user-create", max_age=1*24*60*60)
        user = User.query.filter_by(username=mail_id, is_verified=False).first_or_404()
        user.is_verified = True
        user.password = password
        user.designation = designation
        user.contact = contact
        db.session.commit()
        logout_user()
        return redirect(url_for('html_blueprint.index', info="Added User"))
    else:
        try:
            email = get_token_data(token, salt="user-create", max_age=1*24*60*60)
            user = User.query.filter_by(username=email, is_verified=False).first()
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
        payload = get_token_data(token, salt="team-user", max_age=15*24*60*6)
        team_id, user_id = payload.split(',')
        team_id, user_id = int(team_id), int(user_id)
        db.engine.execute(f'UPDATE User_Team_Mapping SET is_verified = true WHERE team_id = {team_id} AND user_id = {user_id}')
        logout_user()
        return redirect(url_for('html_blueprint.index', info="Added Team"))
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
        mail_id = get_token_data(token, salt="forget-password", max_age=3600)
        user = User.query.filter_by(username=mail_id, type='regular-user').first_or_404()
        user.is_verified = True
        user.password = password
        db.commit()
        logout_user()
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

