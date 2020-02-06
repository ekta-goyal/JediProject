from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

bcrypt = Bcrypt()

def init_crypt(app):
    with app.app_context():
        bcrypt.init_app(app)
        global url_safe_timed_serializer
        url_safe_timed_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def get_time_token(data, salt):
    token = url_safe_timed_serializer.dumps(data, salt=salt)
    return token

def get_token_data(token, salt, max_age=3600):
    data = url_safe_timed_serializer.loads(token, salt=salt, max_age=max_age)
    return data
