import unittest
import nose

from app.models import User


class TestUserAuthentication(unittest.TestCase):
    """This model tests that user passwords are stored hashed
    in the database and can be verified against the user information.
    """

    def test_password_setter(self):
        """.Check password setting."""
        u = User(password_hash='cat')
        self.assertTrue(u.password_hash is not None)

    def test_password_verification(self):
        """Check password verification."""
        u = User(password_hash='cat')
        u.hash_password('cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

if __name__ == '__main__':
    nose.run()
