from flask import Flask

from app.utils import get_config

Config = get_config()


def create_app(config_name=None, **kwargs):
    """
    Entry point to the Flask RESTful Server application.
    """
    from app.database import init_db
    from app.users.views import users_api

    app = Flask(__name__, **kwargs)

    try:
        app.config.from_object(get_config(config_name))
    except ImportError:
        raise Exception('Invalid Config')

    app.register_blueprint(users_api, url_prefix='/api/v1/users/')

    init_db(app)
    return app
