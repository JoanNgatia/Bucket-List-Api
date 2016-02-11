import os


class Config(object):
    """Default configurations."""

    DEBUG = True
    TESTING = False
    # CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']


class TestingConfig(Config):
    """Testing configurations."""

    directory = os.path.dirname(os.path.abspath(__file__))
    test_db = os.path.join(directory, '../tests/test.db')

    TESTING = True
    DATABASE_URL = 'sqlite:///' + test_db


class DevelopmentConfig(Config):
    """
    Development configurations.
    """
    DEVELOPMENT = True
    DEBUG = True
