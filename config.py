import os
try:
    if os.environ["HEROKU"]:
        print("Heroku Platform")
        SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI'] # manditory
        SECRET_KEY = os.environ['SECRET_KEY']
        SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
        SQLALCHEMY_POOL_RECYCLE = os.environ.get('SQLALCHEMY_POOL_RECYCLE', 500)
        SQLALCHEMY_DATABASE_RESET = os.environ.get('SQLALCHEMY_DATABASE_RESET', False)

        FLASK_ADMIN_SWATCH = os.environ.get('FLASK_ADMIN_SWATCH', 'Flatly')
except KeyError:
    try:
        import config_vars
        SQLALCHEMY_DATABASE_URI = config_vars.SQLALCHEMY_DATABASE_URI
        SQLALCHEMY_TRACK_MODIFICATIONS = config_vars.SQLALCHEMY_TRACK_MODIFICATIONS
        SQLALCHEMY_POOL_RECYCLE = config_vars.SQLALCHEMY_POOL_RECYCLE
        SQLALCHEMY_DATABASE_RESET = config_vars.SQLALCHEMY_DATABASE_RESET

        FLASK_ADMIN_SWATCH = config_vars.FLASK_ADMIN_SWATCH
        SECRET_KEY = config_vars.SECRET_KEY

    except:
        print("Some Error")