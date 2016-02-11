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
        self.assertEqual(response.status_code == 400)


if __name__ == '__main__':
    nose.run()
