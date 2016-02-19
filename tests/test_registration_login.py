
from flask import url_for
import json
from werkzeug.security import generate_password_hash, check_password_hash

from test_base import BaseTestCase
from app.models import User
from app.database import session

from faker import Factory

fake = Factory.create()


class SignUpViewTests(BaseTestCase):
    """This class contains all tests for user creation and signin."""

    def setUp(self):
        """Instantiate dummy test details."""
        self.username = fake.user_name()
        self.password = fake.password()
        password_hash = generate_password_hash(self.password)
        self.user = User(username=self.username, password_hash=password_hash)
        session.add(self.user)
        session.commit()

    def test_user_registration(self):
        """Test that creation of a user succeeds when correct info is sent."""
        username = fake.user_name()
        password = fake.password()
        response = self.client.post(url_for('register'),
                                    data=json.dumps({'username': username,
                                                     'password': password}),
                                    content_type='application/json')
        self.assertIn('User {} has been successfully registered'.
                      format(username), response.data)
        self.assertEqual(response.status_code, 201)

    def test_registration_no_password(self):
        """Test that a user is not allowed to register without a password."""
        response = self.client.post(url_for('register'),
                                    data=json.dumps({'username': self.username}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing fields!', response.data)

    def test_registration_no_username(self):
        """Test that a user cannot register without a username."""
        response = self.client.post(url_for('register'),
                                    data=json.dumps({'password': self.password}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing fields!', response.data)

    def test_user_login(self):
        """Test that a user can successfuly login."""
        response = self.client.post(url_for('login'),
                                    data=json.dumps({'username': self.username,
                                                     'password': self.password}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
