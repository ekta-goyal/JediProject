from flask import Flask, jsonify
from flask_sqlalchemy import event
from app.database import db
def create_app(config_name=None, **kwargs):
    """
    Entry point to the Flask RESTful Server application.
    """
    from app.database     import init_db
    from app.loginmanager import init_login_manager
    from app.crypt        import init_crypt
    from app.admin        import init_admin
    from app.mail         import init_mail

    from app.workforce.api import api_blueprint
    from app.workforce.web import html_blueprint
    from app.workforce.verify import verify_blueprint
    from app.admin import admin_html_blueprint
    
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration

    app = Flask(__name__, **kwargs)

    try:
        app.config.from_pyfile('../config.py')
    except ImportError:
        raise Exception('Invalid Config')

    app.register_blueprint(api_blueprint, url_prefix='/api/v1/')
    app.register_blueprint(admin_html_blueprint, url_prefix='/admin/')
    app.register_blueprint(verify_blueprint, url_prefix='/verify')
    app.register_blueprint(html_blueprint, url_prefix='/')

    init_db(app)
    init_login_manager(app)
    init_crypt(app)
    init_mail(app)
    init_admin(app)

    sentry_sdk.init(
        dsn=app.config['SENTRY_DSN'],
        integrations=[FlaskIntegration()]
    )
    
    from flask_cors import CORS
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    print(app.url_map)

    print("Database Reset:", app.config['SQLALCHEMY_DATABASE_RESET'])
    SAMPLE_DATA = app.config['SQLALCHEMY_DATABASE_RESET']
    if SAMPLE_DATA:
        add_data(app)

    return app

def add_data(app):
    from models import User, Team, Task
    from app.database import db
    print("Inserting Sample Data")
    with app.app_context():
        a1, a2, a3 = (
            User(
                name='Nitheesh Chandra',
                username="Nitheesh",
                password="nith@123",
                type='admin'
            ),
            User(
                name='Vishaka Shah',
                username="Vishaka",
                password="vish@123",
                type='admin'
            ),
            User(
                name='Ekta Goyal',
                username="Ekta",
                password="ekta@123",
                type='admin'
            )
        )

        u1, u2, u3 = (
            User(
                name='User1',
                username="user1@test.com",
                password="password",
                type='regular-user',
                is_verified=True
            ),
            User(
                name='User2',
                username="user2@test.com",
                password="password",
                type='regular-user',
                is_verified=True
            ),
            User(
                name='User3',
                username="user3@test.com",
                password="password",
                type='regular-user',
                is_verified=False
            )
        )


        t1, t2 = (
            Team(
                name='Team1',
                description='''t is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).'''
            ),
            Team(
                name='Team2',
                description='''Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'''
            )
        )
        
        print("Adding Default values")
        db.session.add_all([a1, a2, a3])
        print("Added admins, now test users...")
        db.session.add_all([u1, u2, u3])
        db.session.commit()
        print("Added user values")

        print("Adding Team values...")
        db.session.add_all([t1, t2])
        db.session.commit()
        print("Added Team values...")

        print("PRINTING".center(10,"-"))
        t1.members.append(u1)
        t1.members.append(u2)
        t1.members.append(u3)
        t2.members.append(u3)
        db.session.commit()

        u2.teams.append(t2)
        db.session.commit()

        from sqlalchemy.sql import func
        task1 = Task(
            title = "Task1",
            description = "Some random text",
            start_date = '2020-01-25',
            expected_end_date = '2020-02-10',
            task_status = 'TODO',
            priority = 'medium'

        )
        task1.team = t1
        task1.reporter = u2
        task1.assignee = u1
        task4 = Task(
            title = "Task4",
            description = "Some random text",
            start_date = '2020-01-25',
            expected_end_date = '2020-02-10',
            task_status = 'TODO',
            priority = 'medium'

        )
        task4.team = t1
        task4.reporter = u2
        task4.assignee = u1

        task2 = Task(
            title = "Task2",
            description = "Some more random text",
            start_date = '2020-01-25',
            expected_end_date = '2020-02-10',
            task_status = 'DOING',
            priority = 'high'

        )
        task2.team = t1
        task2.reporter = u1
        task2.assignee = u2
        task5 = Task(
            title = "Task5",
            description = "Some random text",
            start_date = '2020-01-25',
            expected_end_date = '2020-02-10',
            task_status = 'TODO',
            priority = 'medium'

        )
        task5.team = t1
        task5.reporter = u1
        task5.assignee = u2

        task3 = Task(
            title = "Task3",
            description = "for Team3",
            start_date = '2020-01-25',
            expected_end_date = '2020-02-10',
            task_status = 'DONE',
            priority = 'low'

        )
        task3.team = t1
        task3.reporter = u2
        task3.assignee = u1

        db.session.add_all([task1, task2, task3, task4, task5])
        db.session.commit()
        from models import UserSchema, TeamSchema, TaskSchema
        from pprint import pprint
        import json
        # pprint(json.loads(jsonify(UserSchema().dump(u2)).data))
        # pprint(json.loads(jsonify(UserSchema().dump(u1)).data))
        # pprint(json.loads(jsonify(UserSchema().dump(u3)).data))
        # print('NEW'.center(50,'-'))
        # pprint(json.loads(jsonify(UserSchema(many=True).dump(t2.members)).data))
        # print('Task'.center(50,'-'))
        # pprint(json.loads(jsonify(TaskSchema().dump(task1)).data))