from flask import url_for, g
import json
from werkzeug.security import generate_password_hash

from test_base import BaseTestCase
from app.models import User, BucketList
from app.database import session

from faker import Factory

fake = Factory.create()


class TestBucketLists(BaseTestCase):
    """Tests against bucketlist creation and retrieval."""

    def setUp(self):
        """Instantiate dummy bucketlist details for testing."""
        # create a dummy user
        self.username = fake.user_name()
        self.password = fake.password()
        password_hash = generate_password_hash(self.password)
        self.user = User(username=self.username, password_hash=password_hash)
        session.add(self.user)
        session.commit()

        # create a dummy bucketlist
        self.list_name = 'Ein Schatz finden'
        self.bucketlist = BucketList(list_name=self.list_name,
                                     creator=self.user.user_id)
        session.add(self.bucketlist)
        session.commit()

        # log in a user to retrieve token
        self.response = self.client.post(url_for('login'),
                                         data=json.dumps({
                                             'username': self.username,
                                             'password': self.password}),
                                         content_type='application/json')
        self.token = json.loads(self.response.data)['token']

    def tearDown(self):
        """Delete details created at end of test."""
        del self.username
        del self.password
        del self.user
        del self.bucketlist
        del self.token
        session.remove()

    def test_unauthorized_bucketlist_methods(self):
        """Test unsuccessful bucketlist retrieval and  /
        creation for unauthorized users."""
        response = self.client.get(url_for('bucketlists'))
        self.assertEqual(response.status_code, 401)

        response = self.client.post(url_for('bucketlists'))
        self.assertEqual(response.status_code, 401)

    def test_bucketlist_creation(self):
        """Test successful bucketlist creation."""
        bucketlist1 = {
            'list_name': fake.name()
        }

        response = self.client.post(url_for('bucketlists'), data=bucketlist1,
                                    headers={'token': self.token})
        self.assertEqual(response.status, '201 CREATED')
        self.assertIn(bucketlist1['list_name'], response.data)

    def test_bucketlist_retrieval(self):
        """Test successful bucketlist retrieval."""
        response = self.client.get(url_for('bucketlists'),
                                   headers={'token': self.token})
        self.assertEqual(response.status, '200 OK')
        self.assertIn(self.list_name, response.data)

    def test_bucketlist_manipulation_by_id(self):
        """Test that a user can get or delete a specific bucketlist."""

        url = '/bucketlists/{}/'.format(self.bucketlist.list_id)

        # Test user can get bucketlist by ID
        response = self.client.get(url,
                                   headers={'token': self.token})
        self.assertEqual(response.status_code, 200)

        # Test a user can delete a particular bucketlist
        response = self.client.delete(url,
                                      headers={'token': self.token})
        self.assertEqual(response.status_code, 204)

    def test_bucketlist_search_by_name(self):
        """Test that a user can search for a bucketlist by its name."""
        list_name = 'Ins Kino gehen'
        bucketlist = BucketList(list_name=list_name,
                                creator=self.user.user_id)
        session.add(bucketlist)
        session.commit()

        response = self.client.get('/bucketlists/?q=Kino',
                                   headers={'token': self.token})
        self.assertIn('Kino', response.data)
        self.assertEqual(response.status_code, 200)
