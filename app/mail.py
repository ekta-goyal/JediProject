from flask_mail import Mail
from threading import Thread
from flask_mail import Message

mail = Mail()

def init_mail(app):
    with app.app_context():
        mail.init_app(app)
        

def _async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

@_async
def send_async_email(app, recipients, subject, body=None,html=None):
    with app.app_context():
        msg = Message(subject, recipients=recipients)
        msg.body = body
        msg.html = html
        mail.send(msg)
        print("Mail Sent")
