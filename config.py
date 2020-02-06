import os
try:
    if os.environ["HEROKU"]:
        print("Heroku Platform")
        SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI'] # manditory
        SECRET_KEY = os.environ['SECRET_KEY']
        SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False))
        SQLALCHEMY_POOL_RECYCLE = int(os.environ.get('SQLALCHEMY_POOL_RECYCLE', 500))
        SQLALCHEMY_DATABASE_RESET = bool(os.environ.get('SQLALCHEMY_DATABASE_RESET', False))

        FLASK_ADMIN_SWATCH = os.environ.get('FLASK_ADMIN_SWATCH', 'Flatly')

        BCRYPT_LOG_ROUNDS = int(os.environ['BCRYPT_LOG_ROUNDS'])

        # Mail
        MAIL_SERVER = os.environ['MAIL_SERVER']
        MAIL_PORT = int(os.environ['MAIL_PORT'])
        MAIL_USERNAME = os.environ['MAIL_USERNAME']
        MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
        MAIL_DEFAULT_SENDER = os.environ['MAIL_DEFAULT_SENDER']
        MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', False)
        
        SENTRY_DSN = os.environ.get('SENTRY_DSN')
except KeyError:
    try:
        print("Local config")
        import config_vars
        SQLALCHEMY_DATABASE_URI = config_vars.SQLALCHEMY_DATABASE_URI
        SQLALCHEMY_TRACK_MODIFICATIONS = config_vars.SQLALCHEMY_TRACK_MODIFICATIONS
        SQLALCHEMY_POOL_RECYCLE = config_vars.SQLALCHEMY_POOL_RECYCLE
        SQLALCHEMY_DATABASE_RESET = config_vars.SQLALCHEMY_DATABASE_RESET

        FLASK_ADMIN_SWATCH = config_vars.FLASK_ADMIN_SWATCH
        SECRET_KEY = config_vars.SECRET_KEY
        
        # Bcrypt algorithm hashing rounds
        # BCRYPT_LOG_ROUNDS = config_vars.BCRYPT_LOG_ROUNDS

        # Mail
        MAIL_SERVER = config_vars.MAIL_SERVER
        MAIL_PORT = config_vars.MAIL_PORT
        MAIL_USERNAME = config_vars.MAIL_USERNAME
        MAIL_PASSWORD = config_vars.MAIL_PASSWORD
        MAIL_DEFAULT_SENDER = config_vars.MAIL_DEFAULT_SENDER
        MAIL_USE_SSL = config_vars.MAIL_USE_SSL

        SENTRY_DSN = config_vars.SENTRY_DSN
    except Exception as e:
        print("Some Error", e)