from flask_sqlalchemy import SQLAlchemy, event


db = SQLAlchemy()


def init_db(app):
    with app.app_context():
        db.init_app(app)
        from pprint import pprint
        pprint(app.config)
        if app.config.get('SQLALCHEMY_DATABASE_RESET', False):
            print("Deleating Database")
            db.reflect()
            db.drop_all()
            print("Delete Database")
        db.create_all()
        print("Database Ready")