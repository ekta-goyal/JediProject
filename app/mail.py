from flask_mail import Mail

mail = Mail()


def init_mail(app):
    with app.app_context():
        mail.init_app(app)