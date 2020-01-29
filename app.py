from flask import Flask
import config
# from workforceapp.models import migrate



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
#
#
# #Creating a migrate object
# migrate = Migrate(workforceapp, db)
#


if __name__ == '__main__':

    app.run()
