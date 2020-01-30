from flask_login import LoginManager

login_manager = LoginManager()


def init_login_manager(app):
    with app.app_context():
        login_manager.init_app(app)
