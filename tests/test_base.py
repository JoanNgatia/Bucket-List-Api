import os
import unittest
import sqlite3
import json
import nose

from flask import g, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from faker import Factory
# from app.manage import app
from app.models import Base, User
from main.manage import create_app, db

fake = Factory.create()

class TestBase(unittest.TestCase):
    username = fake.user_name()
    password = fake.password()

    def setUp(self):
        # import ipdb
        # ipdb.set_trace()

        """Set up test database environment."""
        app = create_app('testing')
        self.app = app

        # # self.dbfile = self.app.config.get('DATABASE_URL')[10:]
        # self.dbfile = self.app.config.get('DATABASE_URL')
        # sqlite3.connect(self.dbfile)
        # set current flask context for request handling during testing
        self.app_context = self.app.app_context()
        self.app_context.push()
        with self.app_context:
            db.init_app(self.app)
            db.create_all()
        # create a dummy client to send requests to the server
        self.client = app.test_client()

    def test_registration_without_password(self):
        """Test registration with no password."""
        # import ipdb; ipdb.set_trace()
        response = self.client.post('/register',
                                    data=json.dumps({'username': self.username}), content_type='application/json')

        # import ipdb; ipdb.set_trace()
        self.assertTrue(response.status_code == 400)
    # def tearDown(self):
    #     """Clean up after tests."""
    # # delete test db after testing
    #     os.remove(self.dbfile)
    #     # db.session.remove()
        # db.drop_all()

if __name__ == '__main__':
    nose.run()
