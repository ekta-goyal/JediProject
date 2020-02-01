from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def init_crypt(app):
    with app.app_context():
        bcrypt.init_app(app)
