import unittest
import nose

from app.models import User


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password_hash='cat')
        self.assertTrue(u.password_hash is not None)

    def test_password_verification(self):
        u = User(password_hash='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

if __name__ == '__main__':
    nose.run()
