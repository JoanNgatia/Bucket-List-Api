import nose

from flask.ext.testing import TestCase
from config.config import TestingConfig

from main.manage import app, db
from app.database import session, init_db, Base


class BaseTestCase(TestCase):
    """A base test case for flask-tracking."""

    def create_app(self):
        """method for setting up config variables for the app"""
        app.config.from_object(TestingConfig)
        return app

    def setUp(self):
        """setUp method"""
        self.app = app.test_client()
        # db.create_all()
        init_db()

    def tearDown(self):
        """method for clearing all settings"""
        session.remove()
        # Base.drop_all()
        # Base.remove()
        # Base.drop_all()

if __name__ == '__main__':
    nose.run()
