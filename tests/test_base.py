import os
import unittest
import sqlite3
# import json
import nose

from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker


# from app.manage import app
# from app.models import Base, User
from main.manage import create_app


class TestBase(unittest.TestCase):

    def setUp(self):
        """Set up test database environment."""
        app = create_app('testing')
        self.app = app

        # configure app with test settings
        self.dbfile = self.app.config.get('DATABASE_URL')[10:]
        sqlite3.connect(self.dbfile)

        # configure dummy engine to dump models in test database
        # test_engine = create_engine(self.app.config.get('DATABASE_URL'))
        # import ipdb; ipdb.set_trace()
        # Base.metadata.create_all(test_engine)
        # Session = sessionmaker(bind=test_engine)
        # session = scoped_session(Session)

        # create a dummy client to send requests to the server
        self.client = self.app.test_client()

    # def tearDown(self):
    #     """Clean up after tests."""
    #     # delete test db after testing
    #     os.remove(self.dbfile)

if __name__ == '__main__':
    nose.run()
