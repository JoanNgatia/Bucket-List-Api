import os
import unittest
import sqlite3
from sqlalchemy import create_engine

from app.manage import app
from app.models import Base


class TestBase(unittest.TestCase):

    def setUp(self):
        """Set up test database environment."""
        self.app = app

        # store default state of db before modifications
        self.development_settings = os.environ['APP_SETTINGS']
        os.environ['APP_SETTINGS'] = 'config.config.TestingConfig'

        # configure app with test settings
        self.app.config.from_object(os.environ['APP_SETTINGS'])
        self.dbfile = self.app.config.get('DATABASE_URL')[10:]
        sqlite3.connect(self.dbfile)

        # configure dummy engine to dump models in test database
        test_engine = create_engine(self.app.config.get('DATABASE_URL'))
        Base.metadata.create_all(test_engine)

        # create a dummy client to send requests to the server
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up after tests."""

        # delete test db after testing
        os.remove(self.dbfile)

        # revert app setting to default state
        os.environ['APP_SETTINGS'] = self.development_settings
        app.config.from_object(os.environ['APP_SETTINGS'])
