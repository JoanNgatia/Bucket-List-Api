import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask.ext.restful import Api
from flask.ext.login import LoginManager
from itsdangerous import TimedJSONWebSignatureSerializer as \
    Serializer, BadSignature, SignatureExpired

from app.authentication import UserRegistration, UserLogin
from app.resources import BucketListAll, BucketListId, \
    BucketListItemAdd, BucketListItemEdit
# from app.db import session
from app.models import User

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_type):
    """Initialize flask application."""
    app = Flask(__name__)
    app.config.from_object(config.config[config_type])
    db.init_app(app)
    return app

app = create_app('default')
api = Api(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.request_loader
def load_user(request):
    """Check authorization header and authenticate user for request.

    Authenticate user with provided token where the login_required
    decorator is used
    """
    token = request.headers.get('token')

    if token:
        s = Serializer(os.environ.get('SECRET_KEY'))
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = session.query(User).get(data['confirm'])
        return user
    return None

api.add_resource(UserRegistration, '/auth/register/')
api.add_resource(UserLogin, '/auth/login/')
api.add_resource(BucketListAll, '/bucketlists/')
api.add_resource(BucketListId, '/bucketlists/<list_id>/')
api.add_resource(BucketListItemAdd, '/bucketlist/<list_id>/item/')
api.add_resource(BucketListItemEdit, '/bucketlist/<list_id>/item/<item_id>/')

if __name__ == '__main__':
    manager.run()
