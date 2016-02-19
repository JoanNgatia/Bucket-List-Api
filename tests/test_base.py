import nose

from flask.ext.testing import TestCase
from config.config import TestingConfig

from main.manage import app
from app.database import session, init_db


class BaseTestCase(TestCase):
    """A base test case for flask-tracking."""

    def create_app(self):
        """method for setting up config variables for the app"""
        app.config.from_object(TestingConfig)
        return app

    def setUp(self):
        """setUp method"""
        self.app = app.test_client()
        init_db()

    def tearDown(self):
        """method for clearing all settings"""
        session.remove()

if __name__ == '__main__':
    nose.run()
