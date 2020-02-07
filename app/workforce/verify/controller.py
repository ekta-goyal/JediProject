from flask import request, redirect, url_for, render_template, Blueprint
from itsdangerous import SignatureExpired, BadTimeSignature
from http import HTTPStatus
from models import User
from app.database import db

verify_blueprint = Blueprint('verify_blueprint', __name__, template_folder='templates')

@verify_blueprint.route('/user/<token>')
def confirm_email(token): 
    from app.crypt import get_token_data
    try:
        email = get_token_data(token, salt="user-create", max_age=3600)
        user = User.query.filter_by(username=email).first()

        if user.is_verified:
            return 'Already Validated'
        else:
            user.is_verified = True
            db.session.commit()
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
