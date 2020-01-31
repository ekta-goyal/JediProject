_database_type = 'mysql'
_database_name = 'UiMqjofMZs'
_host = 'remotemysql.com'
_port = 3306
_username = 'UiMqjofMZs'
_password = 'jotF0yQvTt'

# URI : 'mysql://UiMqjofMZs:jotF0yQvTt@remotemysql.com:3306/UiMqjofMZs'
SQLALCHEMY_DATABASE_URI = f'{_database_type}://{_username}:{_password}@{_host}:{_port}/{_database_name}'
SQLALCHEMY_TRACK_MODIFICATIONS = True

FLASK_ADMIN_SWATCH = 'Flatly'
SECRET_KEY = 'mysecret'
