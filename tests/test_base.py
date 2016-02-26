import nose

from flask.ext.testing import TestCase
from config.config import TestingConfig

from main.manage import app, db
from app.database import init_db


class BaseTestCase(TestCase):
    """A base test case for flask-application testing."""

    def create_app(self):
        """Set up config variables for the test Flask app."""
        app.config.from_object(TestingConfig)
        return app

    def setUp(self):
        """Setup flask app for testing."""
        self.app = app.test_client()
        init_db()

    def tearDown(self):
        """Method for clearing all settings."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    nose.run()
