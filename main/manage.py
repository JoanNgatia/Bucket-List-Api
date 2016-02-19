import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask.ext.login import LoginManager
from itsdangerous import TimedJSONWebSignatureSerializer as \
    Serializer, BadSignature, SignatureExpired
import sys
import inspect

from app.api.authentication import UserRegistration, UserLogin, UserLogout
from app.resources import BucketListAll, BucketListId, \
    BucketListItemAdd, BucketListItemEdit
from app.database import session
from app.models import User

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from config import config

currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

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

api.add_resource(UserRegistration, '/auth/register/', endpoint='register')
api.add_resource(UserLogin, '/auth/login/', endpoint='login')
api.add_resource(UserLogout, '/auth/logout/', endpoint='logout')
api.add_resource(BucketListAll, '/bucketlists/', endpoint='bucketlists')
api.add_resource(BucketListId, '/bucketlists/<list_id>/',
                 endpoint='single_bucketlist')
api.add_resource(BucketListItemAdd, '/bucketlist/<list_id>/item/',
                 endpoint='bucketlistitems')
api.add_resource(
    BucketListItemEdit, '/bucketlist/<list_id>/item/<item_id>/',
    endpoint='single_bucketlistitem')

if __name__ == '__main__':
    manager.run()
