from flask import Flask

def create_app(config_name=None, **kwargs):
    """
    Entry point to the Flask RESTful Server application.
    """
    from app.database import init_db

    from app.loginmanager import init_login_manager
    from app.workforceapp.controller import regular_api_blueprint, regular_html_blueprint
    from app.workforceapp.controller import admin_html_blueprint, admin

    app = Flask(__name__, **kwargs)

    try:
        app.config.from_pyfile('../config.py')
    except ImportError:
        raise Exception('Invalid Config')

    app.register_blueprint(regular_api_blueprint, url_prefix='/api/v1/')
    app.register_blueprint(regular_html_blueprint, url_prefix='/')
    app.register_blueprint(admin_html_blueprint, url_prefix='/admin/')

    init_db(app)
    init_login_manager(app)
    admin.init_app(app)
    return app