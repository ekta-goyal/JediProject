import os
try:
    if os.environ["HEROKU"]:
        print("Heroku Platform")
        SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
        SQLALCHEMY_TRACK_MODIFICATIONS = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']

        FLASK_ADMIN_SWATCH = os.environ['FLASK_ADMIN_SWATCH']
        SECRET_KEY = os.environ['SECRET_KEY']
except KeyError:
    try:
        import config_vars
        SQLALCHEMY_DATABASE_URI = config_vars.SQLALCHEMY_DATABASE_URI
        SQLALCHEMY_TRACK_MODIFICATIONS = config_vars.SQLALCHEMY_TRACK_MODIFICATIONS

        FLASK_ADMIN_SWATCH = config_vars.FLASK_ADMIN_SWATCH
        SECRET_KEY = config_vars.SECRET_KEY
    except:
        print("Some Error")