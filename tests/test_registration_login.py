import nose
import json

from test_base import TestBase
# from app.models import User


class TestUserAuthentication(TestBase):
    # defaultusername = 'Archer'
    # defaultpassword = 'Sterling'

    def test_registration_without_password(self):
        """Test registration with no password."""
        response = self.client.post(
            '/auth/register/', data=json.dumps({'username': 'Archer'}))
        self.assertFalse(response.status_code == 400)

    def test_registration_without_username(self):
        """test for user registration with no username provided."""
        response = self.client.post(
            '/auth/register/', data=json.dumps({'password': 'Sterling'}))
        self.assertFalse(response.status_code == 400)

    def test_user_successful_login(self):
        response = self.client.post(
            '/auth/login/', data=json.dumps({
                'username': 'lele', 'password': 'cats'}))
        self.assertFalse(response.status_code == 200)


class TestUserBucketListCreation(TestBase):

    def test_succesful_bucketlist_creation(self):
        response = self.client.post(
            '/bucketlists/', data=json.dumps({
                'list_name': 'Find a bae for Kiki'}))
        self.assertEqual(response.status_code, 201)

    def test_successful_bucketlistitem_creation(self):
        response = self.client.post(
            '/bucketlists/1/items/', data=json.dumps({
                'item_name': 'Create website bae for kiki'
            }))
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    nose.run()
