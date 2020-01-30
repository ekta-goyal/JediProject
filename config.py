from os.path import join, dirname, abspath


class BaseConfig:
    DEBUG = False
    PROJECT_ROOT = abspath(dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{join(PROJECT_ROOT, "db.sqlite3")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True
    DOMAIN = 'http://localhost:5000'


class TestingConfig(BaseConfig):
    ENV = 'testing'
    TESTING = True
    DOMAIN = 'http://testserver'

    # Use memory for DB files
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
